import time


class BrokenPromiseError(Exception):
    pass


class _Promise(object):

    def __init__(self):
        self._value = None

    def set_value(self, value):
        self._value = value

    def get_future(self):
        return self


def wg_await(*args, **kwargs):
    return None


def wg_async(func):

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def delay(seconds):
    time.sleep(seconds)