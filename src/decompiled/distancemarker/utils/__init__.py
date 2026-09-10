# uncompyle6 version 3.9.2
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.8.10 (tags/v3.8.10:3d8993a, May  3 2021, 11:48:03) [MSC v.1928 64 bit (AMD64)]
# Embedded file name: src\distancemarker\utils\__init__.py
# Compiled at: 2024-02-29 22:38:16
import logging
from BWUtil import AsyncReturn
from gui import DialogsInterface
from gui.Scaleform.daapi.view.dialogs import SimpleDialogMeta, I18nInfoDialogButtons
from realm import CURRENT_REALM
from wg_async import wg_async, _Promise, wg_await, BrokenPromiseError, delay
logger = logging.getLogger(__name__)

def overrideIn(cls, condition=lambda : True):

    def _overrideMethod(func):
        if not condition():
            return func
        funcName = func.__name__
        if funcName.startswith('__'):
            funcName = '_' + cls.__name__ + funcName
        old = getattr(cls, funcName)

        def wrapper(*args, **kwargs):
            return func(old, *args, **kwargs)

        setattr(cls, funcName, wrapper)
        return wrapper

    return _overrideMethod


def addMethodTo(cls, condition=(lambda : True)):

    def _overrideMethod(func):
        if not condition():
            return func
        setattr(cls, func.__name__, func)
        return func

    return _overrideMethod


def getClientType():
    return CURRENT_REALM


def isClientWG():
    return not isClientLesta()


def isClientLesta():
    return CURRENT_REALM == 'RU'


@wg_async
def displayDialog(message):
    while True:
        try:
            yield await_callback_param(DialogsInterface.showDialog, callbackParamName='callback')(SimpleDialogMeta(title='Distance Marker', message=message, buttons=I18nInfoDialogButtons(i18nKey='common/error')))
            break
        except BrokenPromiseError:
            logger.warning('Cannot display dialog yet, try next second')
            yield wg_await(delay(1.0))
            continue
        except Exception:
            logger.warning('Failed to display warning dialog window.', exc_info=True)
            break


def await_callback_param(func, timeout=None, callbackParamName='callback'):

    def wrapper(*args, **kwargs):
        promise = _Promise()

        def callback(*args):
            if len(args) == 1:
                args = args[0]
            promise.set_value(args)

        kwargs[callbackParamName] = callback
        func(*args, **kwargs)
        return wg_await(promise.get_future(), timeout)

    return wrapper


class ObservingSemaphore(object):

    def __init__(self):
        self.observerCount = 0

    def __enter__(self):
        self.observerCount += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.observerCount -= 1

    def __nonzero__(self):
        return self.observerCount > 0

    def withIgnoringLock(self, returnForIgnored):

        def _withIgnoringLock(func):

            def wrapper(*args, **kwargs):
                if self:
                    return returnForIgnored
                with self:
                    return func(*args, **kwargs)

            return wrapper

        return _withIgnoringLock

    def withAsyncIgnoringLock(self, returnForIgnored):

        def _withAsyncIgnoringLock(func):

            @wg_async
            def wrapper(*args, **kwargs):
                if self:
                    raise AsyncReturn(returnForIgnored)
                with self:
                    result = yield wg_await(func(*args, **kwargs))
                    raise AsyncReturn(result)

            return wrapper

        return _withAsyncIgnoringLock
