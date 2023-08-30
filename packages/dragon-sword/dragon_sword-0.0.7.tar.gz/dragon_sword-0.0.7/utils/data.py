import logging
import re
import os
import zlib
import pickle
from abc import ABCMeta
from collections import defaultdict
import hashlib
from typing import Any
from threading import Lock
import uuid
from utils.system import cur_pid, cur_tid
from utils.log import logger


def md5(text):
    encode_pwd = text.encode()
    md5_pwd = hashlib.md5(encode_pwd)
    return md5_pwd.hexdigest()


def str_to_int(s: str):
    m = md5(s)
    return int(m, 16)


def is_num(s) -> bool:
    return isinstance(s, int) or isinstance(s, float) or s.replace('.', '', 1).isdigit()


def uniq_id() -> str:
    return uuid.uuid1().hex


def decode_gzip(b: bytes) -> bytes:
    try:
        return zlib.decompress(b, 16 + zlib.MAX_WBITS)
    except zlib.error:
        return b


def decode_bytes(b: bytes) -> tuple[str, bool]:
    try:
        return b.decode("utf-8"), True
    except UnicodeDecodeError:
        return "", False


def get_ints_in_str(s: str) -> list[int]:
    ss = re.findall(r'\d+', s)
    result = []
    for s in ss:
        if is_num(s):
            result.append(int(s))
    return result


class Cache:
    """
    大多数基础类型赋值操作都是线程安全的，本类主要是为了防止并发重复加载
    """

    def __init__(self):
        self._lock = Lock()
        self._inited = False

    def _load(self):
        """
        从配置中加载数据项
        :return:
        """
        raise Exception("Cache._load not implemented")

    def _get(self, key: str):
        return getattr(self, key, None)

    def _init_data(self):
        if self._inited:
            return
        with self._lock:
            if self._inited:
                return
            self._load()
            self._print()
            self._inited = True

    def get(self, key: str):
        self._init_data()
        return self._get(key)

    def __str__(self) -> str:
        _d = self.__dict__
        return {k: v for k, v in _d.items() if k != "_lock"}.__str__()

    def _print(self):
        s = f"{self.__class__.__name__} in {cur_pid()} {cur_tid()} data={self}"
        logger.debug(s)


class CacheKey:
    """
    本类在key加载时加锁，保证每条key数据的一致性
    """

    def __init__(self):
        self._lock = Lock()  # 对_key_lock和_cache_data操作时加锁
        self._key_lock: dict[str, Lock] = {}  # 单key加载时加锁
        self._cache_data: dict[str, Any] = {}

    def _get_lock(self, key: str) -> Lock:
        lock = self._key_lock.get(key)
        if lock:
            return lock
        with self._lock:
            lock = self._key_lock.get(key)
            if lock:
                return lock
            lock = Lock()
            self._key_lock[key] = lock
            return lock

    def _key_inited(self, key: str):
        return key in self._cache_data

    def _load(self, key: str):
        """
        key没有缓存时，加载数据项
        :return:
        """
        raise Exception("CacheKey._load not implemented")

    def _del(self, key: str):
        # 防止并发删除异常
        if not self._key_inited(key):
            return
        with self._lock:
            if not self._key_inited(key):
                return
            del self._cache_data[key]

    def _get(self, key: str):
        # 基础类型保证thread-safe
        return self._cache_data.get(key, None)

    def _init_data(self, key: str):
        if self._key_inited(key):
            return
        with self._get_lock(key):
            if self._key_inited(key):
                return
            r = self._load(key)
            if r is None:
                return
            self._cache_data[key] = r

    def get(self, key: str):
        self._init_data(key)
        return self._get(key)

    def del_key(self, key: str):
        return self._del(key)

    def update(self, key: str, info=None):
        """
        更新仅删除，交由get重新加载数据
        :param key:
        :param info:
        :return:
        """
        return self.del_key(key)


def load_file_lock():
    def lock(file, flags):
        pass

    def unlock(file):
        pass

    return

    # TODO: pywin install fail
    if os.name == 'nt':
        import win32con, win32file, pywintypes

        LOCK_EX = win32con.LOCKFILE_EXCLUSIVE_LOCK
        LOCK_SH = 0  # The default value
        LOCK_NB = win32con.LOCKFILE_FAIL_IMMEDIATELY
        __overlapped = pywintypes.OVERLAPPED()

        def lock(file, flags):
            hfile = win32file._get_osfhandle(file.fileno())
            win32file.LockFileEx(hfile, flags, 0, 0xffff0000, __overlapped)

        def unlock(file):
            hfile = win32file._get_osfhandle(file.fileno())
            win32file.UnlockFileEx(hfile, 0, 0xffff0000, __overlapped)
    elif os.name == 'posix':
        from fcntl import flock, LOCK_UN

        def lock(file, flags):
            flock(file.fileno(), flags)

        def unlock(file):
            flock(file.fileno(), LOCK_UN)
    else:
        raise RuntimeError("File Locker only support NT and Posix platforms!")


load_file_lock()


def store(data, key):
    b = pickle.dumps(data)
    with open(key, "wb") as f:
        f.write(b)
    return

    # TODO: no fcntl
    try:
        f = open(key, "wb")
        fcntl.lockf(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        os.truncate(file_desc, 0)
        os.write(file_desc, b)
    except IOError as err:
        logging.exception(err)
    finally:
        os.close(file_desc)
        logging.info(f"close file {file_desc}")


def get_data(key):
    # TODO: add file read lock
    # file_desc = os.open(key, os.O_RDWR)
    if not os.path.isfile(key):
        return None
    with open(key, "rb") as f:
        return pickle.load(f)


class VoiceAsrData(metaclass=ABCMeta):
    def __init__(self, asr_data: dict):
        self._asr_data = asr_data

    def parse(self):
        pass

    def sentences(self):
        pass


class Time:
    def __init__(self, start, end):
        self.begin = start
        self.end = end


class Sentence:
    def __init__(self, speaker, seg_id):
        self.time = Time(0, 0)
        self.text = ""
        self.speaker = speaker
        self.xf_seg_id = seg_id

    def time_begin(self, begin):
        self.time.begin = begin

    def time_end(self, end):
        self.time.end = end

    def add_text(self, word: str):
        self.text = f"{self.text}{word}"

    def __str__(self):
        return f"{self.time.begin}-{self.time.end} {self.speaker}: {self.text}"


class Content:
    def __init__(self):
        self._c: [Sentence] = []
        self._speaker_c = defaultdict(list)
        self._time_c = defaultdict(list)

    def add(self, s: Sentence):
        self._c.append(s)
        self._speaker_c[s.speaker].append(s)
        self._time_c[s.time].append(s)

    def add_punc(self, punc: str, speaker: str) -> bool:
        """
        标点符号在话语结束后的下一句一起返回
        """
        if len(self._c) == 0:
            return False
        if self._c[-1].speaker != speaker:
            return False
        self._c[-1].text += punc
        return True

    def __str__(self):
        return "\n".join([str(item) for item in self._c])


class LowStr(str):
    def __new__(cls, s: str):
        return str.__new__(cls, s.lower())
