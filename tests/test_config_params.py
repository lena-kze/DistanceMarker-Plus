import unittest

import _support
from _support import set_language, reset_params


class TestConfigParams(unittest.TestCase):

    def setUp(self):
        set_language('de')
        reset_params()

    def test_registered_params_count(self):
        from distancemarker.settings.config_param import g_configParams
        from distancemarker.settings.config_param_types import PARAM_REGISTRY
        self.assertEqual(len(list(g_configParams.items())), 27)
        self.assertEqual(len(PARAM_REGISTRY), 27)

    def test_mod_language_options(self):
        from distancemarker.settings.config_param import g_configParams, ModLanguage
        self.assertEqual(ModLanguage.EN, 'en')
        self.assertEqual(ModLanguage.DE, 'de')
        param = g_configParams.modLanguage
        self.assertEqual(param.defaultValue, 'de')
        self.assertEqual(param.value, 'de')
        self.assertEqual(param(), 'de')
        self.assertEqual([option.value for option in param.options], [ModLanguage.EN, ModLanguage.DE])
        self.assertEqual([option.displayName for option in param.options], ['Englisch', 'Deutsch'])
        self.assertEqual([option.msaValue for option in param.options], [0, 1])

    def test_mod_language_msa_round_trip(self):
        from distancemarker.settings.config_param import g_configParams
        param = g_configParams.modLanguage
        self.assertEqual(param.toMsaValue('de'), 1)
        self.assertEqual(param.toMsaValue('en'), 0)
        self.assertEqual(param.fromMsaValue(1), 'de')
        self.assertEqual(param.fromMsaValue(0), 'en')
        self.assertEqual(param.msaValue, 1)
        self.assertEqual(param.defaultMsaValue, 1)
        self.assertEqual(param.defaultJsonValue, '"de"')

    def test_zone_color_defaults(self):
        from distancemarker.settings.config_param import g_configParams
        self.assertEqual(g_configParams.textColor.defaultValue, (255, 11, 0))
        self.assertEqual(g_configParams.nearDistanceColor.defaultValue, (0, 153, 255))
        self.assertEqual(g_configParams.zone3DistanceColor.defaultValue, (255, 11, 0))
        self.assertEqual(g_configParams.zone4DistanceColor.defaultValue, (255, 11, 0))
        self.assertEqual(g_configParams.zone5DistanceColor.defaultValue, (255, 11, 0))
        self.assertEqual(g_configParams.farDistanceColor.defaultValue, (255, 229, 0))

    def test_color_param_json_round_trip(self):
        from distancemarker.settings.config_param import g_configParams
        param = g_configParams.zone3DistanceColor
        param.jsonValue = [1, 2, 3]
        self.assertEqual(param.value, (1, 2, 3))
        self.assertEqual(param.jsonValue, '[1, 2, 3]')
        param.msaValue = '010203'
        self.assertEqual(param.value, (1, 2, 3))
        self.assertEqual(param.msaValue, '010203')
        self.assertEqual(param.fromJsonValue([10, 20, 30]), (10, 20, 30))
        self.assertEqual(param.toJsonValue((10, 20, 30)), '[10, 20, 30]')

    def test_zone_color_token_names(self):
        from distancemarker.settings.config_param import g_configParams
        self.assertEqual(g_configParams.zone3DistanceColor.tokenName, 'zone3-distance-color')
        self.assertEqual(g_configParams.zone4DistanceColor.tokenName, 'zone4-distance-color')
        self.assertEqual(g_configParams.zone5DistanceColor.tokenName, 'zone5-distance-color')

    def test_clamping_of_color_values(self):
        from distancemarker.settings import toColorTuple
        self.assertEqual(toColorTuple([-1, 300, 51]), (0, 255, 51))

    def test_disabled_param_returns_disabled_value(self):
        from distancemarker.settings.config_param import g_configParams
        g_configParams.textSize.value = 20
        self.assertEqual(g_configParams.textSize(), 20)
        g_configParams.enabled.value = False
        self.assertEqual(g_configParams.textSize(), 11)
        g_configParams.enabled.value = True
        self.assertEqual(g_configParams.textSize(), 20)

    def test_default_config_tokens_match_registry(self):
        from distancemarker.settings import getDefaultConfigTokens
        from distancemarker.settings.config_param import g_configParams
        tokens = getDefaultConfigTokens()
        self.assertEqual(set(tokens.keys()), set(tokenName for tokenName, param in g_configParams.items()))
        self.assertEqual(tokens['mod-language'], '"de"')
        self.assertEqual(tokens['zone3-distance-color'], '[255, 11, 0]')
        self.assertEqual(tokens['zone4-distance-color'], '[255, 11, 0]')
        self.assertEqual(tokens['zone5-distance-color'], '[255, 11, 0]')

    def test_missing_config_key_reads_as_none(self):
        from distancemarker.settings.config_param import g_configParams
        self.assertIsNone(g_configParams.zone3DistanceColor.readValueFromConfigDict({}))
        self.assertEqual(g_configParams.zone3DistanceColor.readValueFromConfigDictSafely({}), (255, 11, 0))
