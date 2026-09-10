# uncompyle6 version 3.9.2
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.8.10 (tags/v3.8.10:3d8993a, May  3 2021, 11:48:03) [MSC v.1928 64 bit (AMD64)]
# Embedded file name: src\distancemarker\settings\config.py
# Compiled at: 2024-02-29 22:38:16
from distancemarker.settings import getDefaultConfigTokens, ConfigException
from distancemarker.settings.config_file import g_configFiles
from distancemarker.settings.config_param import g_configParams
from distancemarker.settings.migrations import performConfigMigrations
from distancemarker.utils import *
logger = logging.getLogger(__name__)

class Config(object):
    fileSemaphore = ObservingSemaphore()

    def __init__(self):
        self.__loadedSuccessfully = False

    @fileSemaphore.withIgnoringLock(returnForIgnored=None)
    def reloadSafely(self):
        try:
            self.__loadConfigFileToParams()
            self.__updateModSettingsApiIfPresent()
        except ConfigException as e:
            logger.warning('Failed to load (or create) config')
            displayDialog(e.message)
        except Exception:
            logger.error('Failed to load (or create) config due to unknown error.', exc_info=True)
            displayDialog('Failed to load (or create) config due to unknown error.\nContact mod developer for further support with provided logs.')

    def persistParamsSafely(self):
        try:
            rawSerializedSettings = {tokenName: param.jsonValue for tokenName, param in g_configParams.items()}
            self.updateConfigSafely(rawSerializedSettings)
            self.__updateModSettingsApiIfPresent()
        except Exception:
            logger.error('Failed to save updated marker position offset.', exc_info=True)

    @fileSemaphore.withIgnoringLock(returnForIgnored=None)
    def updateConfigSafely(self, rawSerializedSettings):
        if not self.__loadedSuccessfully:
            displayDialog('Configuration saving cancelled, because last performed manual config load failed.\nCorrect any typos in config file and restart game before trying to use GUI.')
            return
        try:
            self.__prepareConfigFilesSafely()
            logger.info('Starting config saving ...')
            serializedSettings = getDefaultConfigTokens()
            serializedSettings.update(rawSerializedSettings)
            g_configFiles.config.writeConfigTokens(serializedSettings)
            logger.info('Finished config saving.')
            self.__loadConfigFileToParams()
            self.__updateModSettingsApiIfPresent()
        except ConfigException as e:
            logger.error('Failed to save config file')
            displayDialog(e.message)
        except Exception:
            logger.error('Failed to save config file due to unknown reason.', exc_info=True)
            displayDialog('Failed to save config file due to unknown reason.\nContact mod developer for further support with provided logs.')

    def __loadConfigFileToParams(self):
        logger.info('Starting config loading ...')
        self.__loadedSuccessfully = False
        self.__prepareConfigFiles()
        configDict = g_configFiles.config.loadConfigDict()
        for tokenName, param in g_configParams.items():
            value = param.readValueFromConfigDict(configDict)
            value = value if value is not None else param.defaultValue
            param.jsonValue = value

        self.__loadedSuccessfully = True
        self.__handleLanguageChange()
        logger.info('Finished config loading.')
        return

    @staticmethod
    def __handleLanguageChange():
        from distancemarker.settings.translations import reloadTranslations
        from helpers import getClientLanguage
        if reloadTranslations(getClientLanguage()):
            from distancemarker import g_distanceMarkerMod
            if g_distanceMarkerMod.isModsSettingsApiPresent:
                from distancemarker.support.mods_settings_api_support import refreshSettingsPage
                refreshSettingsPage()

    def __prepareConfigFilesSafely(self):
        try:
            self.__prepareConfigFiles()
        except ConfigException:
            logger.error('Failed to prepare config files, but continue anyway.')
        except Exception:
            logger.error('Failed to prepare config files, but continue anyway.', exc_info=True)

    def __prepareConfigFiles(self):
        performConfigMigrations()
        g_configFiles.createMissingConfigFiles()

    @staticmethod
    def __updateModSettingsApiIfPresent():
        from distancemarker import g_distanceMarkerMod
        if g_distanceMarkerMod.isModsSettingsApiPresent:
            from distancemarker.support.mods_settings_api_support import onConfigFileReload
            from distancemarker.support.mods_settings_api_support import settingsChangedSemaphore
            with settingsChangedSemaphore:
                onConfigFileReload()


g_config = Config()
