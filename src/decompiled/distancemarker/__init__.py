# uncompyle6 version 3.9.2
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.8.10 (tags/v3.8.10:3d8993a, May  3 2021, 11:48:03) [MSC v.1928 64 bit (AMD64)]
# Embedded file name: src\distancemarker\__init__.py
# Compiled at: 2024-02-29 22:38:16
import logging
logger = logging.getLogger(__name__)

class DistanceMarkerMod(object):

    @property
    def isModsSettingsApiPresent(self):
        return self.__isModsSettingsApiPresent

    def __init__(self):
        self.__isModsSettingsApiPresent = False

    def init(self):
        try:
            logger.info('Initializing DistanceMarker mod ...')
            from distancemarker.utils import getClientType
            logger.info('Client type: %s', getClientType())
            from distancemarker.settings import translations
            translations.loadTranslations()
            import distancemarker.hooks
            self.__resolveSoftDependenciesSafely()
            if self.isModsSettingsApiPresent:
                from distancemarker.support import mods_settings_api_support
                mods_settings_api_support.registerSoftDependencySupport()
            from distancemarker.settings.config import g_config
            g_config.reloadSafely()
            logger.info('DistanceMarker mod initialized')
        except Exception:
            logger.error('Error occurred while initializing DistanceMarker mod', exc_info=True)
            from distancemarker.utils import displayDialog
            displayDialog('Error occurred while initializing DistanceMarker mod.\nContact mod developer with error logs for further support.')

    def __resolveSoftDependenciesSafely(self):
        try:
            from gui.modsSettingsApi import g_modsSettingsApi
            self.__isModsSettingsApiPresent = g_modsSettingsApi is not None
            if not self.isModsSettingsApiPresent:
                logger.warn('Error probably occurred in ModsSettingsAPI because it is None, ignore its presence.')
        except ImportError:
            self.__isModsSettingsApiPresent = False
        except Exception:
            logger.warn('Error occurred in ModsSettingsAPI, ignore its presence.', exc_info=True)
            self.__isModsSettingsApiPresent = False

        return

    def fini(self):
        pass


g_distanceMarkerMod = DistanceMarkerMod()
