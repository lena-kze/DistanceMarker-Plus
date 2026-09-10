import json
import os
import unittest

import _support
from _support import set_language, reset_params, temp_cwd, set_msa_present
from distancemarker.settings.config import g_config
from distancemarker.settings.config_file import g_configFiles
from distancemarker.settings.config_param import g_configParams

CONFIG_RELATIVE_PATH = os.path.join('mods', 'configs', 'DistanceMarker', 'config.json')


class TestConfig(unittest.TestCase):

    def setUp(self):
        set_language('de')
        reset_params()
        set_msa_present(False)

    def tearDown(self):
        set_msa_present(False)

    def test_default_config_is_created(self):
        with temp_cwd() as tmpDir:
            self.assertFalse(g_configFiles.config.exists())
            g_config.reloadSafely()
            self.assertTrue(os.path.isfile(os.path.join(tmpDir, CONFIG_RELATIVE_PATH)))
            self.assertTrue(g_config._Config__loadedSuccessfully)
            self.assertEqual(g_configParams.enabled.value, True)
            self.assertEqual(g_configParams.modLanguage.value, 'de')
            self.assertEqual(g_configParams.textColor.value, (255, 11, 0))
            self.assertEqual(g_configParams.zone3DistanceColor.value, (255, 11, 0))
            self.assertEqual(g_configParams.zone4DistanceColor.value, (255, 11, 0))
            self.assertEqual(g_configParams.zone5DistanceColor.value, (255, 11, 0))
            self.assertEqual(g_configParams.nearDistanceColor.value, (0, 153, 255))
            self.assertEqual(g_configParams.farDistanceColor.value, (255, 229, 0))

    def test_custom_values_are_loaded_and_language_switches(self):
        with temp_cwd() as tmpDir:
            g_config.reloadSafely()
            configDict = g_configFiles.config.loadConfigDict()
            configDict['text-size'] = 12
            configDict['text-color'] = [1, 2, 3]
            configDict['near-distance-color'] = [0, 0, 0]
            configDict['zone5-distance-color'] = [9, 9, 9]
            configDict['enabled'] = False
            with open(CONFIG_RELATIVE_PATH, 'w') as configFile:
                configFile.write(json.dumps(configDict))

            g_config.reloadSafely()

            self.assertTrue(g_config._Config__loadedSuccessfully)
            self.assertEqual(g_configParams.textSize.value, 12)
            self.assertEqual(g_configParams.textColor.value, (1, 2, 3))
            self.assertEqual(g_configParams.nearDistanceColor.value, (0, 0, 0))
            self.assertEqual(g_configParams.zone5DistanceColor.value, (9, 9, 9))
            self.assertEqual(g_configParams.modLanguage.value, 'de')
            self.assertEqual(g_configParams.enabled.value, False)
            from distancemarker.settings import translations
            self.assertEqual(translations.CURRENT_LANGUAGE, 'de')

    def test_invalid_config_does_not_crash(self):
        with temp_cwd() as tmpDir:
            os.makedirs(os.path.dirname(CONFIG_RELATIVE_PATH))
            with open(CONFIG_RELATIVE_PATH, 'w') as configFile:
                configFile.write('{ not valid json !!!')
            g_config.reloadSafely()
            self.assertFalse(g_config._Config__loadedSuccessfully)

    def test_msa_settings_are_synced_on_reload(self):
        with temp_cwd() as tmpDir:
            set_msa_present(True)
            from gui import modsSettingsApi
            modsSettingsApi.msa_fake.settings = {}
            g_config.reloadSafely()
            self.assertTrue(g_config._Config__loadedSuccessfully)
            self.assertEqual(modsSettingsApi.msa_fake.updateLinkage, 'com.github.pruszko.distancemarker')
            self.assertTrue(len(modsSettingsApi.msa_fake.settings) > 0)
            for tokenName, param in g_configParams.items():
                self.assertEqual(modsSettingsApi.msa_fake.settings[tokenName], param.msaValue,
                                 msg='MSA setting mismatch for %s' % tokenName)

    def test_persist_params_safely_updates_file(self):
        with temp_cwd() as tmpDir:
            g_config.reloadSafely()
            g_configParams.textColor.value = (1, 2, 3)
            g_configParams.zone3DistanceColor.value = (9, 9, 9)
            g_configParams.drawDistanceUnit.value = True

            g_config.persistParamsSafely()

            configDict = g_configFiles.config.loadConfigDict()
            self.assertEqual(configDict['text-color'], [1, 2, 3])
            self.assertEqual(configDict['zone3-distance-color'], [9, 9, 9])
            self.assertEqual(configDict['draw-distance-unit'], True)
            self.assertEqual(configDict['__version__'], 5)

    def test_flatten_fills_missing_tokens_with_defaults(self):
        with temp_cwd() as tmpDir:
            tokens = g_configFiles.config.flattenConfigDictToTokens({})
            self.assertEqual(tokens['imprecise-display-mode'], '"except-view-range"')
            self.assertEqual(tokens['mod-language'], '"de"')
            self.assertIn('enabled', tokens)
            self.assertIn('near-distance-color', tokens)

    def test_write_failure_keeps_previous_file_content(self):
        with temp_cwd() as tmpDir:
            g_config.reloadSafely()
            before = g_configFiles.config.loadConfigDict()
            with self.assertRaises(Exception):
                g_configFiles.config.writeConfigTokens({'enabled': 'true'})
            after = g_configFiles.config.loadConfigDict()
            self.assertEqual(before, after)
