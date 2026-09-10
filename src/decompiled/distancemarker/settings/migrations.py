# uncompyle6 version 3.9.2
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.8.10 (tags/v3.8.10:3d8993a, May  3 2021, 11:48:03) [MSC v.1928 64 bit (AMD64)]
# Embedded file name: src\distancemarker\settings\migrations.py
# Compiled at: 2025-06-19 21:35:36
import os, logging
from distancemarker.settings import copy, deleteEmptyFolderSafely, toBool, ConfigException
from distancemarker.settings.config_file import g_configFiles
logger = logging.getLogger(__name__)

class ConfigVersion(object):
    V2_1_0 = 1
    V2_2_0 = 2
    V3_0_0 = 3
    V4_0_0 = 4
    V5_0_0 = 5
    CURRENT = V5_0_0


def performConfigMigrations():
    try:
        if not g_configFiles.config.exists():
            return
        configDict = g_configFiles.config.loadConfigDict()
        if isVersion(configDict, ConfigVersion.CURRENT):
            return
        v2_2_0_addTextOutlineAndDistanceUnitParameters(configDict)
        v3_0_0_addLanguageAndZoneColorParameters(configDict)
        v4_0_0_replaceImpreciseSymbolSwitch(configDict)
        v5_0_0_addDarstellungsbereichSummand(configDict)
        g_configFiles.config.writeConfigDict(configDict)
    except ConfigException:
        logger.error('Failed to perform config file migration.')
        raise
    except Exception:
        logger.error('Failed to perform config file migration.', exc_info=True)
        raise ConfigException('Failed to perform config file migration due to unknown error.\nContact mod developer for further support with provided logs.')


def v2_2_0_addTextOutlineAndDistanceUnitParameters(configDict):
    if not isVersion(configDict, ConfigVersion.V2_1_0):
        return
    logger.info('Migrating config file from version 2.1.x to 2.2.x ...')
    configDict['draw-text-outline'] = False
    configDict['draw-distance-unit'] = True
    progressVersion(configDict)
    logger.info('Migration finished.')


def v3_0_0_addLanguageAndZoneColorParameters(configDict):
    if not isVersion(configDict, ConfigVersion.V2_2_0):
        return
    logger.info('Migrating config file from version 2.2.x to 3.0.x ...')
    configDict['mod-language'] = 'de'
    configDict['zone3-distance-color'] = [255, 11, 0]
    configDict['zone4-distance-color'] = [255, 11, 0]
    configDict['zone5-distance-color'] = [255, 11, 0]
    configDict.setdefault('show-imprecise-symbol', True)
    progressVersion(configDict)
    logger.info('Migration finished.')


def v4_0_0_replaceImpreciseSymbolSwitch(configDict):
    if not isVersion(configDict, ConfigVersion.V3_0_0):
        return
    logger.info('Migrating config file from version 3.x to 4.0.x ...')
    if 'imprecise-display-mode' not in configDict:
        configDict['imprecise-display-mode'] = 'except-view-range' if configDict.get('show-imprecise-symbol', True) else 'always-numbers'
    oldBonuses = [int(configDict.get(tokenName, 0)) for tokenName in ('size-bonus-zone1', 'size-bonus-zone2', 'size-bonus-zone3', 'size-bonus-zone4', 'size-bonus-zone5')]
    if oldBonuses in ([7, 5, 4, 3, 2], [7, 12, 16, 19, 21]):
        newBonuses = [21, 19, 16, 12, 7]
        for index, tokenName in enumerate(('size-bonus-zone1', 'size-bonus-zone2', 'size-bonus-zone3', 'size-bonus-zone4', 'size-bonus-zone5')):
            configDict[tokenName] = newBonuses[index]
    configDict.pop('show-imprecise-symbol', None)
    progressVersion(configDict)
    logger.info('Migration finished.')


def v5_0_0_addDarstellungsbereichSummand(configDict):
    if not isVersion(configDict, ConfigVersion.V4_0_0):
        return
    logger.info('Migrating config file from version 4.x to 5.0.x ...')
    configDict.setdefault('size-bonus-zone6', 0)
    if [int(configDict.get(tokenName, 0)) for tokenName in ('size-bonus-zone1', 'size-bonus-zone2', 'size-bonus-zone3', 'size-bonus-zone4', 'size-bonus-zone5')] == [7, 12, 16, 19, 21]:
        for tokenName, value in zip(('size-bonus-zone1', 'size-bonus-zone2', 'size-bonus-zone3', 'size-bonus-zone4', 'size-bonus-zone5'), (21, 19, 16, 12, 7)):
            configDict[tokenName] = value
    progressVersion(configDict)
    logger.info('Migration finished.')


def progressVersion(configDict):
    if '__version__' not in configDict:
        configDict['__version__'] = ConfigVersion.V2_1_0
        return
    configDict['__version__'] = int(configDict['__version__']) + 1


def isVersion(configDict, version):
    if '__version__' not in configDict:
        return ConfigVersion.V2_1_0 == version
    return int(configDict['__version__']) == version
