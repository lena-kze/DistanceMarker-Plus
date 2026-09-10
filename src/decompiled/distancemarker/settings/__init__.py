# uncompyle6 version 3.9.2
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.8.10 (tags/v3.8.10:3d8993a, May  3 2021, 11:48:03) [MSC v.1928 64 bit (AMD64)]
# Embedded file name: src\distancemarker\settings\__init__.py
# Compiled at: 2024-02-29 22:38:16
import json, logging, os
logger = logging.getLogger(__name__)

class ConfigException(Exception):
    pass


def getDefaultConfigTokens():
    from distancemarker.settings.config_param import g_configParams
    return {tokenName: param.defaultJsonValue for tokenName, param in g_configParams.items()}


def toJson(obj):
    return json.dumps(obj, encoding='UTF-8')


def toBool(value):
    return str(value).lower() == 'true'


def toPositiveFloat(value):
    floatValue = float(value)
    if floatValue > 0.0:
        return floatValue
    return 0.0


def clamp(minValue, value, maxValue):
    if minValue is not None:
        value = max(minValue, value)
    if maxValue is not None:
        value = min(value, maxValue)
    return value


def toColorTuple(value):
    if len(value) != 3:
        raise Exception('Provided color array does not have exactly 3 elements.')
    rawRed = int(value[0])
    rawGreen = int(value[1])
    rawBlue = int(value[2])
    red = clamp(0, rawRed, 255)
    green = clamp(0, rawGreen, 255)
    blue = clamp(0, rawBlue, 255)
    return (red, green, blue)


def copy(oldPath, newPath):
    with open(oldPath, 'r') as oldFile:
        oldRawData = oldFile.read()
        with open(newPath, 'w') as newFile:
            newFile.write(oldRawData)


def createFolderSafely(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def deleteEmptyFolderSafely(path):
    try:
        os.rmdir(path)
    except OSError:
        pass
