import asyncio
from multiprocessing import Process, Queue
from threading import Thread, Event
from queue import Empty
from typing import Any
import signal
import os
import traceback
from functools import wraps
from utils.errno import Error, OK
from utils.time import get_now_stamp_float, get_stamp_after
from utils.log import logger
from utils.system import is_linux


class Context:
    def __init__(self, timeout, start=get_now_stamp_float()):
        self._start = start
        self._deadline = get_stamp_after(self._start, second=timeout)
        self.timeout = timeout

    def timeoutd(self, now=get_now_stamp_float()) -> bool:
        return now >= self._deadline


def init_before_server(conf_path: str, in_put: Queue, output: Queue, signal: Queue, log: Queue) -> Error:
    from utils.config import init_conf
    err = init_conf(conf_path)
    if not err.ok:
        return err

    # TODO: remove signal q
    QManager.init_task_q(in_put, output)
    QManager.init_signal_q(signal)
    QManager.init_log_q(log)

    # 初始化日志
    from utils.log import log
    from utils.config import log_conf
    log.init(log_conf())
    return OK


class _QManager:
    def __init__(self):
        super().__init__()
        self.in_q: Queue
        self.out_q: Queue
        self.signal_q: Queue
        self.log_q: Queue
        self._qs = ("in_q", "out_q", "signal_q", "log_q")

        self._log_q_stop = Event()
        self.start_log()

    def init_log_q(self, q: Queue):
        self.log_q = q

    def init_task_q(self, input: Queue, output: Queue):
        self.in_q = input
        self.out_q = output

    def init_signal_q(self, q: Queue):
        self.signal_q = q

    def close(self):
        for q in self._qs:
            if not hasattr(self, q):
                continue
            o = getattr(self, q)
            o.close()
            o.join_thread()

    def empty_task(self):
        self.in_q = Queue()
        self.out_q = Queue()

    def add_task(self, item, timeout=30 * 60):
        self.in_q.put((item, Context(timeout)))

    def get_task(self) -> type[Any, Context]:
        try:
            item, ctx = self.in_q.get()
        except Empty:
            logger.error("QManager get_task q empty")
            return None, None
        return item, ctx

    def get_a_task(self) -> type[Any, Context]:
        item, ctx = self.in_q.get_nowait()
        return item, ctx

    def log(self, s):
        self._log_q_stop.wait()
        self.log_q.put_nowait(s)

    # 原来是为了暂停写日志，目前不需要
    def pause_log(self):
        self._log_q_stop.clear()

    def start_log(self):
        self._log_q_stop.set()

    def log_empty(self) -> bool:
        return self.log_q.empty()

    @property
    def task_num(self) -> int:
        return self.in_q.qsize()

    def __del__(self):
        self.close()


QManager = _QManager()


class Task:
    def __init__(self, handle, name, *args, **kwargs):
        self.handle = handle
        self.args = args
        self.name = name
        self.kwargs = kwargs
        self.init = kwargs.get("init", None)
        self.end = kwargs.get("end", None)


class _MultiM:
    def __init__(self):
        self._p: dict[str, Task] = {}
        self._rp: dict[int, tuple[Task, Process]] = {}
        self._t: dict[str, Task] = {}
        self._rt: dict[int, tuple[Task, Thread]] = {}
        self._killer: GracefulKiller = None

    def add_p(self, name, handler, *args, **kwargs):
        if name in self._p:
            # logger.info(f"MultiM add_p {name} exist")
            return
        self._p[name] = Task(handler, name, *args, **kwargs)

    def add_t(self, name, handler, *args, **kwargs):
        if name in self._t:
            # logger.info(f"MultiM add_t {name} exist")
            return
        self._t[name] = Task(handler, name, *args, **kwargs)

    @property
    def close(self):
        return self._killer and self._killer.kill_now

    def _decorator(self, func, init, end):
        @wraps(func)
        def _fn(*args, **kwargs):
            GracefulKiller(exit_now=True)
            result = None
            if init:
                init()

            try:
                result = func(*args, **kwargs)
            except ErrGracefulKiller:
                print(f"{os.getpid()} grace exit")
            except Exception:
                print(f"{traceback.format_exc()}")

            if end:
                end()
            return result

        return _fn

    def _new_p(self, task) -> Process:
        if is_linux():
            f = self._decorator(task.handle, task.init, task.end)
        else:
            f = task.handle
        p = Process(
            target=f,
            kwargs=task.kwargs,
            args=task.args
        )
        p.start()
        return p

    def _new_t(self, task) -> Thread:
        if is_linux():
            f = self._decorator(task.handle, task.init, task.end)
        else:
            f = task.handle
        t = Thread(
            target=f,
            name=task.name,
            kwargs=task.kwargs,
            args=task.args,
        )
        t.daemon = True
        t.start()
        return t

    def start(self):
        print(f"start processes in {os.getpid()}")
        self._killer = GracefulKiller(exit_now=True, handle_child_exit=self.restart_child)
        for task in self._p.values():
            p = self._new_p(task)
            self._rp[p.pid] = (task, p)
            print(f"process {task.name} started {p.pid}")

        for task in self._t.values():
            t = self._new_t(task)
            self._rt[t.ident] = (task, t)
            print(f"thread {task.name} started")

        # 这行给控制台看
        print("server start success")

        try:
            asyncio.new_event_loop().run_forever()
        except ErrGracefulKiller:
            print(f"will join child")

        # for tid, task_t in self._rt.items():
        #     _, t = task_t
        #     print(f"join thread")
        #     t.join()

        for pid, task_p in self._rp.items():
            print(f"{pid} joining")
            _, p = task_p
            p.join(3)
            if p.is_alive():
                p.terminate()
            print(f"{pid} joined")

    @staticmethod
    def get_exit_child_pid():
        cpid, _ = os.waitpid(-1, os.WNOHANG)
        return cpid

    def _restart_child_by_pid(self, pid):
        task_p = self._rp.get(pid)
        if not task_p:
            print(f"restart child no {pid}")
            return
        task, p = task_p
        p.terminate()
        p = self._new_p(task)
        self._rp[pid] = (task, p)

    def restart_child(self, sig, frame):
        try:
            if self.close:
                return
            cpid = self.get_exit_child_pid()
            if cpid == 0:
                print(f"no child process was immediately available")
                return
            print(f"child process-{cpid} exceptionally exit")
            self._restart_child_by_pid(cpid)
        except ChildProcessError:
            print(f"child fail")


MultiM = _MultiM()


class ErrGracefulKiller(Exception):
    pass


class GracefulKiller:
    kill_now = False

    def __init__(self, exit_now=True, handle_child_exit=None):
        if not exit_now:
            handler = self._exit_gracefully
        else:
            handler = self._exit_now
        signal.signal(signal.SIGINT, handler)
        signal.signal(signal.SIGTERM, handler)
        if is_linux() and handle_child_exit:
            signal.signal(signal.SIGCHLD, handle_child_exit)

    def _exit_now(self, sig, frame):
        self._exit_gracefully(sig, frame)
        raise ErrGracefulKiller(f'Received signal {sig} on line {frame.f_lineno} in {frame.f_code.co_filename}')

    def _exit_gracefully(self, sig, frame):
        self.kill_now = True


def graceful_exit(clear_func=None):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ErrGracefulKiller as e:
                if clear_func:
                    clear_func()
                print(f"{e}")

        return wrapper

    return decorator
