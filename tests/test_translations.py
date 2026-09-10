# -*- coding: utf-8 -*-
import json
import os
import unittest

import _support
from _support import set_language, set_client_language, TRANSLATIONS_DIR


class TestTranslations(unittest.TestCase):

    def setUp(self):
        set_language('en')

    def test_current_language_and_maps(self):
        from distancemarker.settings import translations as t
        self.assertEqual(t.CURRENT_LANGUAGE, 'en')
        self.assertEqual(t.AVAILABLE_LANGUAGES, ['en', 'de'])
        self.assertEqual(t.LANGUAGE_MAP, {'en': 'Englisch', 'de': 'Deutsch'})

    def test_english_translation_values(self):
        from distancemarker.settings import translations as t
        self.assertEqual(t.Tr.MODNAME, 'DistanceMarker-Plus')
        self.assertEqual(t.Tr.INTRO_LABEL, 'Config file info')
        self.assertEqual(t.Tr.MOD_LANGUAGE_HEADER, 'Language')
        self.assertEqual(t.Tr.DISTANCE_ZONE_COLORS_LABEL, '<b>Distance zones</b>')
        self.assertEqual(t.Tr.ZONE1_INFO_LABEL, '<b>Area 1: proxy spotting area (up to 50 m)</b>')
        self.assertEqual(t.Tr.ZONE6_INFO_LABEL, '<b>Area 3: display area (render distance, above 445 m)</b>')
        self.assertEqual(t.Tr.FOOTER_LABEL, u'Von Lena_Kze in Deutschland gemacht. <3')
        self.assertEqual(t.Tr.ZONE3_DISTANCE_COLOR_HEADER, 'Text color')
        self.assertEqual(t.Tr.ZONE4_DISTANCE_COLOR_HEADER, 'Text color')
        self.assertEqual(t.Tr.ZONE5_DISTANCE_COLOR_HEADER, 'Text color')
        self.assertEqual(t.Tr.SIZE_BONUS_ZONE1_HEADER, 'Standard text size + summand')

    def test_reload_switches_to_german(self):
        from distancemarker.settings import translations as t
        self.assertTrue(t.reloadTranslations('de'))
        self.assertEqual(t.CURRENT_LANGUAGE, 'de')
        self.assertEqual(t.Tr.MOD_LANGUAGE_HEADER, 'Sprache')
        self.assertEqual(t.Tr.INTRO_LABEL, 'Config-Datei-Info')
        self.assertEqual(t.Tr.DISTANCE_ZONE_COLORS_LABEL, u'<b>Entfernungszonen</b>')
        self.assertEqual(t.Tr.ZONE1_INFO_LABEL, u'<b>Bereich 1: Proxyspotbereich (bis 50 m)</b>')

    def test_switching_back_to_english_clears_cache(self):
        from distancemarker.settings import translations as t
        self.assertTrue(t.reloadTranslations('de'))
        self.assertEqual(t.Tr.MOD_LANGUAGE_HEADER, 'Sprache')
        self.assertTrue(t.reloadTranslations('en'))
        self.assertEqual(t.CURRENT_LANGUAGE, 'en')
        self.assertEqual(t.Tr.MOD_LANGUAGE_HEADER, 'Language')

    def test_reload_same_language_returns_false(self):
        from distancemarker.settings import translations as t
        self.assertFalse(t.reloadTranslations('en'))

    def test_load_falls_back_to_english_for_unknown_language(self):
        from distancemarker.settings import translations as t
        set_client_language('fr')
        t.loadTranslations()
        self.assertEqual(t.CURRENT_LANGUAGE, 'en')

    def test_reload_unknown_language_falls_back_to_english(self):
        from distancemarker.settings import translations as t
        set_language('de')
        self.assertTrue(t.reloadTranslations('fr'))
        self.assertEqual(t.CURRENT_LANGUAGE, 'en')

    def test_translation_lists_are_joined(self):
        from distancemarker.settings import translations as t
        set_language('de')
        introBody = t.Tr.INTRO_BODY
        self.assertIsInstance(introBody, basestring)
        self.assertIn('config.json', introBody)

    def test_all_tr_tokens_exist_in_both_languages(self):
        from distancemarker.settings import translations as t
        allTokens = set()
        for descriptor in t.Tr.__dict__.values():
            if isinstance(descriptor, t.TranslationBase):
                allTokens.add(descriptor._tokenName)
        self.assertGreater(len(allTokens), 0)
        for language in ('en', 'de'):
            jsonPath = os.path.join(TRANSLATIONS_DIR, 'translations_%s.json' % language)
            with open(jsonPath, 'rb') as translationsFile:
                translationsMap = json.load(translationsFile)
            missingTokens = [token for token in sorted(allTokens) if token not in translationsMap]
            self.assertEqual(missingTokens, [], 'Missing %s tokens: %s' % (language, missingTokens))

    def test_every_tr_token_resolves_to_string(self):
        from distancemarker.settings import translations as t
        set_language('de')
        for descriptor in t.Tr.__dict__.values():
            if isinstance(descriptor, t.TranslationBase):
                value = descriptor.__get__(None, t.Tr)
                self.assertIsInstance(value, basestring, msg='Token %s is not a string' % descriptor._tokenName)
