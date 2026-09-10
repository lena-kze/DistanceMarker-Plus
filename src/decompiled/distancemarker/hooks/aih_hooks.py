# uncompyle6 version 3.9.2
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.8.10 (tags/v3.8.10:3d8993a, May  3 2021, 11:48:03) [MSC v.1928 64 bit (AMD64)]
# Embedded file name: src\distancemarker\hooks\aih_hooks.py
# Compiled at: 2025-06-18 18:51:22
from AvatarInputHandler import AvatarInputHandler
from Event import Event
from distancemarker.utils import overrideIn
onMouseEvent = Event()

@overrideIn(AvatarInputHandler)
def handleMouseEvent(func, self, dx, dy, dz):
    result = func(self, dx, dy, dz)
    onMouseEvent(dx, dy)
    return result
