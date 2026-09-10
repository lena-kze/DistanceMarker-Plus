import unittest

import _support
from _support import set_language, reset_params
from distancemarker.flash import _serializeColorTuple, serializeConfigParams
from distancemarker.settings.config_param import g_configParams


class TestFlashSerialization(unittest.TestCase):

    def setUp(self):
        set_language('de')
        reset_params()

    def test_color_tuple_serialization_values(self):
        self.assertEqual(_serializeColorTuple((255, 11, 0)), 0xFF0B00)
        self.assertEqual(_serializeColorTuple((0, 153, 255)), 0x0099FF)
        self.assertEqual(_serializeColorTuple((255, 229, 0)), 0xFFE500)
        self.assertEqual(_serializeColorTuple((255, 0, 0)), 0xFF0000)
        self.assertEqual(_serializeColorTuple((1, 2, 3)), 0x010203)

    def test_default_serialization(self):
        data = serializeConfigParams()
        self.assertEqual(data['text-color'], 0xFF0B00)
        self.assertEqual(data['near-distance-color'], 0x0099FF)
        self.assertEqual(data['zone3-distance-color'], 0xFF0B00)
        self.assertEqual(data['zone4-distance-color'], 0xFF0B00)
        self.assertEqual(data['zone5-distance-color'], 0xFF0B00)
        self.assertEqual(data['far-distance-color'], 0xFFE500)
        self.assertEqual(data['decimal-precision'], 0)
        self.assertEqual(data['text-size'], 11)
        self.assertEqual(data['text-alpha'], 0.9)
        self.assertEqual(data['draw-text-outline'], True)
        self.assertEqual(data['draw-text-shadow'], False)
        self.assertEqual(data['draw-distance-unit'], False)
        self.assertEqual(data['imprecise-display-mode'], 'except-view-range')
        self.assertEqual(data['size-bonus-zone1'], 7)
        self.assertEqual(data['size-bonus-zone2'], 5)
        self.assertEqual(data['size-bonus-zone3'], 4)
        self.assertEqual(data['size-bonus-zone4'], 3)
        self.assertEqual(data['size-bonus-zone5'], 2)
        self.assertEqual(data['size-bonus-zone6'], 0)

    def test_custom_values_are_serialized(self):
        g_configParams.textColor.value = (1, 2, 3)
        g_configParams.zone3DistanceColor.value = (10, 20, 30)
        g_configParams.farDistanceColor.value = (255, 0, 0)
        data = serializeConfigParams()
        self.assertEqual(data['text-color'], 0x010203)
        self.assertEqual(data['zone3-distance-color'], 0x0A141E)
        self.assertEqual(data['far-distance-color'], 0xFF0000)
        self.assertEqual(data['near-distance-color'], 0x0099FF)

    def test_disabled_mod_serializes_defaults(self):
        g_configParams.enabled.value = False
        g_configParams.zone3DistanceColor.value = (1, 1, 1)
        data = serializeConfigParams()
        self.assertEqual(data['zone3-distance-color'], 0xFF0B00)
