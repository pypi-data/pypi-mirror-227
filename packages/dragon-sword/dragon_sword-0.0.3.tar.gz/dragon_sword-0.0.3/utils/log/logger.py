import json
import os.path
import sys

from utils.log.log import LoggingLogger
from utils.log import log

# _Logger: LoggingLogger


def ensure_filepath_and_lineno(**kwargs):
    if 'extra' not in kwargs:
        kwargs['extra'] = {}
    if 'filename' not in kwargs['extra']:
        kwargs['extra']['filename'] = os.path.split(sys._getframe(2).f_code.co_filename)[1]
    if 'lineno' not in kwargs['extra']:
        kwargs['extra']['lineno'] = sys._getframe(2).f_lineno
    return kwargs


def debug(format_str: str, *args, **kwargs):
    try:
        kwargs = ensure_filepath_and_lineno(**kwargs)
        _Logger: LoggingLogger = getattr(log, "_Logger")
        if _Logger:
            _Logger.debug(format_str, *args, **kwargs)
        else:
            print(format_str.format(*args, **kwargs))
    except Exception as err:  # pylint: disable=broad-except
        print("log err! format_str: %s; args: %s; err: %s", format_str, json.dumps(args), repr(err))


def info(format_str: str, *args, **kwargs):
    try:
        kwargs = ensure_filepath_and_lineno(**kwargs)
        _Logger: LoggingLogger = getattr(log, "_Logger")
        if _Logger:
            _Logger.info(format_str, *args, **kwargs)
        else:
            print(format_str.format(*args, **kwargs))
    except Exception as err:  # pylint: disable=broad-except
        print("log err! format_str: %s; args: %s; err: %s", format_str, json.dumps(args), repr(err))


def warning(format_str: str, *args, **kwargs):
    try:
        kwargs = ensure_filepath_and_lineno(**kwargs)
        _Logger: LoggingLogger = getattr(log, "_Logger")
        if _Logger:
            _Logger.warning(format_str, *args, **kwargs)
        else:
            print(format_str.format(*args, **kwargs))
    except Exception as err:  # pylint: disable=broad-except
        print("log err! format_str: %s; args: %s; err: %s", format_str, json.dumps(args), repr(err))


def error(format_str: str, *args, **kwargs):
    try:
        kwargs = ensure_filepath_and_lineno(**kwargs)
        _Logger: LoggingLogger = getattr(log, "_Logger")
        if _Logger:
            _Logger.error(format_str, *args, **kwargs)
        else:
            print(format_str.format(*args, **kwargs))
    except Exception as err:  # pylint: disable=broad-except
        print("log err! format_str: %s; args: %s; err: %s", format_str, json.dumps(args), repr(err))


def fatal(format_str: str, *args, **kwargs):
    try:
        kwargs = ensure_filepath_and_lineno(**kwargs)
        _Logger: LoggingLogger = getattr(log, "_Logger")
        if _Logger:
            _Logger.fatal(format_str, *args, **kwargs)
        else:
            print(format_str.format(*args, **kwargs))
    except Exception as err:  # pylint: disable=broad-except
        print("log err! format_str: %s; args: %s; err: %s", format_str, json.dumps(args), repr(err))
