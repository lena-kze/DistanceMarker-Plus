import os
import unittest
import zlib

import _support
from _support import CONFIG_AS, DISTANCE_MARKER_AS, INTERIM_SWF


class TestActionScript(unittest.TestCase):

    def test_config_as_declares_zone_colors(self):
        with open(CONFIG_AS, 'rb') as sourceFile:
            content = sourceFile.read()
        for field in ('_zone3DistanceColor:int', '_zone4DistanceColor:int', '_zone5DistanceColor:int'):
            self.assertIn(field, content)
        self.assertIn('_impreciseDisplayMode:String', content)

    def test_config_as_deserializes_zone_colors(self):
        with open(CONFIG_AS, 'rb') as sourceFile:
            content = sourceFile.read()
        for token in ('zone3-distance-color', 'zone4-distance-color', 'zone5-distance-color'):
            self.assertIn('param1["%s"]' % token, content)
        self.assertIn('param1["imprecise-display-mode"]', content)

    def test_config_as_exposes_zone_getters(self):
        with open(CONFIG_AS, 'rb') as sourceFile:
            content = sourceFile.read()
        for name in ('zone3DistanceColor', 'zone4DistanceColor', 'zone5DistanceColor'):
            self.assertIn('function get %s()' % name, content)
            self.assertIn('return this._%s;' % name, content)
        self.assertIn('function get impreciseDisplayMode()', content)

    def test_distance_marker_uses_zone_colors(self):
        with open(DISTANCE_MARKER_AS, 'rb') as sourceFile:
            content = sourceFile.read()
        for token in ('this.config.zone3DistanceColor', 'this.config.zone4DistanceColor', 'this.config.zone5DistanceColor'):
            self.assertIn(token, content)
        self.assertIn('this.config.impreciseDisplayMode', content)
        self.assertIn('this.config.textSize + sizeBonus', content)

    def test_distance_marker_distance_boundaries(self):
        with open(DISTANCE_MARKER_AS, 'rb') as sourceFile:
            content = sourceFile.read()
        for boundary in ('param1 <= 50', 'param1 <= 175', 'param1 <= 250', 'param1 <= 300', 'param1 <= 445'):
            self.assertIn(boundary, content)

    def test_swf_contains_zone_color_tokens(self):
        self.assertTrue(os.path.isfile(INTERIM_SWF), msg='SWF not found at %s' % INTERIM_SWF)
        with open(INTERIM_SWF, 'rb') as swfFile:
            data = swfFile.read()
        if data[:3] == 'CWS':
            data = zlib.decompress(data[8:])
        for token in ('zone3-distance-color', 'zone4-distance-color', 'zone5-distance-color'):
            self.assertIn(token, data, msg='SWF is missing token %s' % token)
