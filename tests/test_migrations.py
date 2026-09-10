import json
import os
import unittest

import _support
from _support import set_language, reset_params, temp_cwd
from distancemarker.settings.config_file import g_configFiles
from distancemarker.settings.config_param import g_configParams
from distancemarker.settings import getDefaultConfigTokens
from distancemarker.settings.migrations import (
    ConfigVersion,
    isVersion,
    progressVersion,
    v2_2_0_addTextOutlineAndDistanceUnitParameters,
    v3_0_0_addLanguageAndZoneColorParameters,
    v4_0_0_replaceImpreciseSymbolSwitch,
    v5_0_0_addDarstellungsbereichSummand,
    performConfigMigrations,
)

CONFIG_RELATIVE_PATH = os.path.join('mods', 'configs', 'DistanceMarker', 'config.json')


class TestMigrations(unittest.TestCase):

    def setUp(self):
        set_language('de')
        reset_params()

    def _writeConfig(self, configDict):
        with open(CONFIG_RELATIVE_PATH, 'w') as configFile:
            configFile.write(json.dumps(configDict))

    def _readConfig(self):
        return g_configFiles.config.loadConfigDict()

    @staticmethod
    def _buildVersionedConfig(version):
        configDict = {tokenName: json.loads(param.defaultJsonValue) for tokenName, param in g_configParams.items()}
        configDict['__version__'] = version
        if version <= 1:
            configDict.pop('draw-text-outline')
            configDict.pop('draw-distance-unit')
        if version <= 2:
            configDict.pop('mod-language')
            configDict.pop('zone3-distance-color')
            configDict.pop('zone4-distance-color')
            configDict.pop('zone5-distance-color')
            configDict.pop('imprecise-display-mode')
        return configDict

    def test_config_version_constants(self):
        self.assertEqual(ConfigVersion.V2_1_0, 1)
        self.assertEqual(ConfigVersion.V2_2_0, 2)
        self.assertEqual(ConfigVersion.V3_0_0, 3)
        self.assertEqual(ConfigVersion.V4_0_0, 4)
        self.assertEqual(ConfigVersion.CURRENT, 5)

    def test_is_version_and_progress_version(self):
        configDictWithoutVersion = {'x': 1}
        self.assertTrue(isVersion(configDictWithoutVersion, ConfigVersion.V2_1_0))
        self.assertFalse(isVersion(configDictWithoutVersion, ConfigVersion.V3_0_0))
        progressVersion(configDictWithoutVersion)
        self.assertEqual(configDictWithoutVersion['__version__'], 1)
        progressVersion(configDictWithoutVersion)
        self.assertEqual(configDictWithoutVersion['__version__'], 2)

    def test_v3_migration_adds_new_keys_and_preserves_values(self):
        configDict = {'__version__': 2, 'text-size': 12, 'text-color': [1, 2, 3]}
        v3_0_0_addLanguageAndZoneColorParameters(configDict)
        self.assertEqual(configDict['__version__'], 3)
        self.assertEqual(configDict['mod-language'], 'de')
        self.assertEqual(configDict['zone3-distance-color'], [255, 11, 0])
        self.assertEqual(configDict['zone4-distance-color'], [255, 11, 0])
        self.assertEqual(configDict['zone5-distance-color'], [255, 11, 0])
        self.assertEqual(configDict['show-imprecise-symbol'], True)
        self.assertEqual(configDict['text-size'], 12)
        self.assertEqual(configDict['text-color'], [1, 2, 3])

    def test_v3_migration_preserves_custom_imprecise_symbol_value(self):
        configDict = {'__version__': 2, 'show-imprecise-symbol': False}
        v3_0_0_addLanguageAndZoneColorParameters(configDict)
        self.assertEqual(configDict['__version__'], 3)
        self.assertEqual(configDict['show-imprecise-symbol'], False)

    def test_v3_migration_ignores_non_v2_configs(self):
        configDict = {'__version__': 3}
        v3_0_0_addLanguageAndZoneColorParameters(configDict)
        self.assertEqual(configDict['__version__'], 3)
        self.assertNotIn('mod-language', configDict)
        self.assertNotIn('zone3-distance-color', configDict)

    def test_v2_migration_ignores_non_v1_configs(self):
        configDict = {'__version__': 2}
        v2_2_0_addTextOutlineAndDistanceUnitParameters(configDict)
        self.assertEqual(configDict['__version__'], 2)
        self.assertNotIn('draw-text-outline', configDict)

    def test_migration_no_config_returns_early(self):
        with temp_cwd() as tmpDir:
            self.assertFalse(g_configFiles.config.exists())
            performConfigMigrations()
            self.assertFalse(g_configFiles.config.exists())

    def test_v2_file_migrates_to_v3(self):
        with temp_cwd() as tmpDir:
            os.makedirs(os.path.dirname(CONFIG_RELATIVE_PATH))
            configDict = self._buildVersionedConfig(2)
            configDict['text-size'] = 12
            configDict['text-color'] = [1, 2, 3]
            self._writeConfig(configDict)

            performConfigMigrations()

            migratedConfig = self._readConfig()
            self.assertEqual(migratedConfig['__version__'], 5)
            self.assertEqual(migratedConfig['mod-language'], u'de')
            self.assertEqual(migratedConfig['zone3-distance-color'], [255, 11, 0])
            self.assertEqual(migratedConfig['zone4-distance-color'], [255, 11, 0])
            self.assertEqual(migratedConfig['zone5-distance-color'], [255, 11, 0])
            self.assertEqual(migratedConfig['text-size'], 12)
            self.assertEqual(migratedConfig['text-color'], [1, 2, 3])
            self.assertEqual(migratedConfig['imprecise-display-mode'], 'except-view-range')
            self.assertEqual(migratedConfig['enabled'], True)

    def test_v2_file_without_imprecise_symbol_migrates_cleanly(self):
        with temp_cwd() as tmpDir:
            os.makedirs(os.path.dirname(CONFIG_RELATIVE_PATH))
            configDict = self._buildVersionedConfig(2)
            self._writeConfig(configDict)

            performConfigMigrations()

            migratedConfig = self._readConfig()
            self.assertEqual(migratedConfig['__version__'], 5)
            self.assertEqual(migratedConfig['imprecise-display-mode'], 'except-view-range')
            self.assertEqual(migratedConfig['mod-language'], u'de')

    def test_v1_file_migrates_to_v3(self):
        with temp_cwd() as tmpDir:
            os.makedirs(os.path.dirname(CONFIG_RELATIVE_PATH))
            configDict = self._buildVersionedConfig(1)
            self._writeConfig(configDict)

            performConfigMigrations()

            migratedConfig = self._readConfig()
            self.assertEqual(migratedConfig['__version__'], 5)
            self.assertEqual(migratedConfig['draw-text-outline'], False)
            self.assertEqual(migratedConfig['draw-distance-unit'], True)
            self.assertEqual(migratedConfig['mod-language'], u'de')
            self.assertEqual(migratedConfig['zone3-distance-color'], [255, 11, 0])
            self.assertEqual(migratedConfig['zone4-distance-color'], [255, 11, 0])
            self.assertEqual(migratedConfig['zone5-distance-color'], [255, 11, 0])
            self.assertEqual(migratedConfig['imprecise-display-mode'], 'except-view-range')

    def test_v3_file_is_left_untouched(self):
        with temp_cwd() as tmpDir:
            os.makedirs(os.path.dirname(CONFIG_RELATIVE_PATH))
            configDict = self._buildVersionedConfig(3)
            configDict['mod-language'] = 'en'
            configDict['zone3-distance-color'] = [1, 1, 1]
            self._writeConfig(configDict)

            performConfigMigrations()

            migratedConfig = self._readConfig()
            self.assertEqual(migratedConfig['__version__'], 5)
            self.assertEqual(migratedConfig['mod-language'], u'en')
            self.assertEqual(migratedConfig['zone3-distance-color'], [1, 1, 1])
