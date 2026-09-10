import json
import re
import unittest

import _support
from _support import set_language, reset_params

TOKEN_RE = re.compile(r'%\(([a-zA-Z0-9_\-]+)\)s')


class TestConfigTemplate(unittest.TestCase):

    def setUp(self):
        set_language('de')
        reset_params()

    def test_placeholders_match_registered_params(self):
        from distancemarker.settings.config_template import CONFIG_TEMPLATE
        from distancemarker.settings.config_param import g_configParams
        placeholders = set(TOKEN_RE.findall(CONFIG_TEMPLATE))
        registeredTokens = set(tokenName for tokenName, param in g_configParams.items())
        self.assertEqual(placeholders, registeredTokens)

    def test_template_contains_version_and_new_keys(self):
        from distancemarker.settings.config_template import CONFIG_TEMPLATE
        self.assertIn('"__version__": 5', CONFIG_TEMPLATE)
        for key in ('mod-language', 'zone3-distance-color', 'zone4-distance-color', 'zone5-distance-color'):
            self.assertIn('"%s"' % key, CONFIG_TEMPLATE)

    def test_default_config_is_valid_and_matches_version(self):
        from distancemarker.settings.config_template import CONFIG_TEMPLATE
        from distancemarker.settings import getDefaultConfigTokens
        from distancemarker.settings.migrations import ConfigVersion
        defaultTokens = getDefaultConfigTokens()
        jsonRawData = CONFIG_TEMPLATE % defaultTokens
        jsonData = re.sub('^ *//.*$', '', jsonRawData, flags=re.MULTILINE)
        configDict = json.loads(jsonData)
        self.assertEqual(configDict['__version__'], 5)
        self.assertEqual(ConfigVersion.CURRENT, 5)
        self.assertEqual(configDict['mod-language'], u'de')
        self.assertEqual(configDict['text-color'], [255, 11, 0])
        self.assertEqual(configDict['near-distance-color'], [0, 153, 255])
        self.assertEqual(configDict['zone3-distance-color'], [255, 11, 0])
        self.assertEqual(configDict['zone4-distance-color'], [255, 11, 0])
        self.assertEqual(configDict['zone5-distance-color'], [255, 11, 0])
        self.assertEqual(configDict['far-distance-color'], [255, 229, 0])
