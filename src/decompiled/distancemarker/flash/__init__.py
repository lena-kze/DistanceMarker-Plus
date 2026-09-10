# uncompyle6 version 3.9.2
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.8.10 (tags/v3.8.10:3d8993a, May  3 2021, 11:48:03) [MSC v.1928 64 bit (AMD64)]
# Embedded file name: src\distancemarker\flash\__init__.py
# Compiled at: 2025-06-19 21:09:59
from distancemarker.settings.config_param import g_configParams

def serializeConfigParams():
    return {'decimal-precision': (g_configParams.decimalPrecision()), 
       'text-size': (g_configParams.textSize()), 
       'text-color': (_serializeColorTuple(g_configParams.textColor())), 
       'text-alpha': (g_configParams.textAlpha()), 
       'draw-text-outline': (g_configParams.drawTextOutline()), 
       'draw-text-shadow': (g_configParams.drawTextShadow()), 
       'draw-distance-unit': (g_configParams.drawDistanceUnit()), 
       'near-distance-color': (_serializeColorTuple(g_configParams.nearDistanceColor())), 
       'zone3-distance-color': (_serializeColorTuple(g_configParams.zone3DistanceColor())), 
       'zone4-distance-color': (_serializeColorTuple(g_configParams.zone4DistanceColor())), 
       'zone5-distance-color': (_serializeColorTuple(g_configParams.zone5DistanceColor())), 
       'far-distance-color': (_serializeColorTuple(g_configParams.farDistanceColor())), 
        'imprecise-display-mode': (g_configParams.impreciseDisplayMode()), 
       'size-bonus-zone1': (g_configParams.sizeBonusZone1()), 
       'size-bonus-zone2': (g_configParams.sizeBonusZone2()), 
       'size-bonus-zone3': (g_configParams.sizeBonusZone3()), 
       'size-bonus-zone4': (g_configParams.sizeBonusZone4()), 
        'size-bonus-zone5': (g_configParams.sizeBonusZone5()),
        'size-bonus-zone6': (g_configParams.sizeBonusZone6())}


def _serializeColorTuple(colorTuple):
    red, green, blue = colorTuple
    color = 0
    color |= red << 16
    color |= green << 8
    color |= blue
    return color
