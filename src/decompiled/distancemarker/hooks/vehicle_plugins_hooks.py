# uncompyle6 version 3.9.2
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.8.10 (tags/v3.8.10:3d8993a, May  3 2021, 11:48:03) [MSC v.1928 64 bit (AMD64)]
# Embedded file name: src\distancemarker\hooks\vehicle_plugins_hooks.py
# Compiled at: 2024-02-29 22:38:16
import logging
from gui.Scaleform.daapi.view.battle.shared.markers2d.vehicle_plugins import VehicleMarkerPlugin
from distancemarker.settings.config_param import g_configParams
from distancemarker.utils import overrideIn
from distancemarker.flash.distance_marker_flash import DistanceMarkerFlash
logger = logging.getLogger(__name__)
g_distanceMarkerFlash = None

@overrideIn(VehicleMarkerPlugin)
def start(func, self):
    global g_distanceMarkerFlash
    func(self)
    try:
        if g_distanceMarkerFlash is None and g_configParams.enabled():
            g_distanceMarkerFlash = DistanceMarkerFlash(self._clazz)
            g_distanceMarkerFlash.active(True)
    except:
        logger.error('Failed to create distance marker app', exc_info=True)

    return


@overrideIn(VehicleMarkerPlugin)
def stop(func, self):
    global g_distanceMarkerFlash
    func(self)
    try:
        if g_distanceMarkerFlash is not None:
            g_distanceMarkerFlash.close()
            g_distanceMarkerFlash = None
    except:
        logger.error('Failed to close distance marker app', exc_info=True)

    return
