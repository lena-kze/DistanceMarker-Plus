# -*- coding: utf-8 -*-
import unittest

import _support
from _support import set_language, reset_params, temp_cwd, set_msa_present
from distancemarker.settings.config_param import g_configParams
from distancemarker.settings.config_param_types import (
    BooleanParam,
    OptionsParam,
    StepperParam,
    SliderParam,
    ColorParam,
)


class TestSettingsPage(unittest.TestCase):

    def setUp(self):
        set_language('de')
        reset_params()
        set_msa_present(False)

    def tearDown(self):
        set_msa_present(False)

    def _refreshTemplate(self):
        from distancemarker.support import mods_settings_api_support
        mods_settings_api_support.refreshSettingsPage()
        from gui import modsSettingsApi
        return modsSettingsApi.msa_fake.template

    @staticmethod
    def _controls(template):
        controls = []
        for column in ('column1', 'column2'):
            controls.extend(template.get(column, []))
        return controls

    def test_template_header(self):
        from distancemarker.support import mods_settings_api_support
        from gui import modsSettingsApi
        template = self._refreshTemplate()
        self.assertEqual(modsSettingsApi.msa_fake.linkage, 'com.github.pruszko.distancemarker')
        self.assertEqual(modsSettingsApi.msa_fake.onChanged, mods_settings_api_support.onModSettingsChanged)
        self.assertEqual(template['modDisplayName'], 'DistanceMarker-Plus')
        self.assertEqual(template['enabled'], True)

    def test_language_dropdown(self):
        template = self._refreshTemplate()
        controls = {control['varName']: control for control in self._controls(template) if 'varName' in control}
        self.assertNotIn('mod-language', controls)

    def test_own_options_are_spatially_separated_from_originals(self):
        template = self._refreshTemplate()
        column2 = template['column2']
        varNames = [control['varName'] for control in column2 if 'varName' in control]
        labels = [control['text'] for control in column2 if control.get('type') == 'Label']
        originalVisualTokens = [
            'decimal-precision',
            'text-size',
            'text-alpha',
            'draw-text-outline',
            'draw-text-shadow',
            'draw-distance-unit',
        ]
        ownTokens = [
            'imprecise-display-mode',
            'near-distance-color',
            'size-bonus-zone1',
            'text-color',
            'size-bonus-zone2',
            'zone3-distance-color',
            'size-bonus-zone3',
            'zone4-distance-color',
            'size-bonus-zone4',
            'zone5-distance-color',
            'size-bonus-zone5',
            'far-distance-color',
            'size-bonus-zone6',
        ]
        for index, token in enumerate(originalVisualTokens):
            self.assertEqual(varNames[index], token, msg='Original visual token %s out of order' % token)
        self.assertEqual(varNames.index('imprecise-display-mode'), len(originalVisualTokens),
                         msg='imprecise-display-mode should start the user settings')
        self.assertNotIn('Eigene Einstellungen', labels)
        impreciseControl = [control for control in column2 if control.get('varName') == 'imprecise-display-mode'][0]
        self.assertNotIn('Standardwert', impreciseControl['tooltip'])
        self.assertFalse(any('_____' in (text or '') for text in labels), msg='Separator underscores must not be used')
        self.assertIn(u'<b>Entfernungszonen</b>', labels)
        zoneLabels = [label for label in labels if label.startswith('<b>Bereich ')]
        self.assertEqual(zoneLabels, [
            u'<b>Bereich 1: Proxyspotbereich (bis 50 m)</b>',
            u'<b>Bereich 2: Sichtbereich (Sichtweite, 51-175 m)</b>',
            u'<b>Bereich 2: Sichtbereich (Sichtweite, 176-250 m)</b>',
            u'<b>Bereich 2: Sichtbereich (Sichtweite, 251-300 m)</b>',
            u'<b>Bereich 2: Sichtbereich (Sichtweite, 301-445 m)</b>',
            u'<b>Bereich 3: Darstellungsbereich (Renderdistanz, über 445 m)</b>',
        ])
        ownStart = len(originalVisualTokens)
        self.assertEqual(varNames[ownStart:ownStart + len(ownTokens)], ownTokens)
        self.assertEqual(len(varNames), ownStart + len(ownTokens))

    def test_footer_is_at_the_end_of_the_page(self):
        import re
        template = self._refreshTemplate()
        last = template['column2'][-1]
        self.assertEqual(last['type'], 'Label')
        visibleText = re.sub(r'</?font[^>]*>', '', last['text']).replace('&lt;', '<')
        self.assertEqual(visibleText, u'Von Lena_Kze in Deutschland erstellt. <3')
        self.assertGreaterEqual(last['text'].count('<font color='), 10, msg='Footer should be rainbow colored')

    def test_distance_zone_color_choices(self):
        template = self._refreshTemplate()
        controls = {control['varName']: control for control in self._controls(template) if 'varName' in control}
        expectedColors = {
            'near-distance-color': '0099FF',
            'text-color': 'FF0B00',
            'zone3-distance-color': 'FF0B00',
            'zone4-distance-color': 'FF0B00',
            'zone5-distance-color': 'FF0B00',
            'far-distance-color': 'FFE500',
        }
        for tokenName, expectedHex in expectedColors.items():
            self.assertIn(tokenName, controls, msg='Missing color control %s' % tokenName)
            self.assertEqual(controls[tokenName]['type'], 'ColorChoice')
            self.assertEqual(controls[tokenName]['value'], expectedHex,
                             msg='Unexpected default color for %s' % tokenName)

    def test_every_registered_param_has_a_control(self):
        template = self._refreshTemplate()
        controls = {control['varName']: control for control in self._controls(template) if 'varName' in control}
        typeMap = {
            BooleanParam: 'CheckBox',
            OptionsParam: 'Dropdown',
            StepperParam: 'NumericStepper',
            SliderParam: 'Slider',
            ColorParam: 'ColorChoice',
        }
        for tokenName, param in g_configParams.items():
            if tokenName in ('enabled', 'mod-language'):
                continue
            self.assertIn(tokenName, controls, msg='No settings control for %s' % tokenName)
            self.assertEqual(controls[tokenName]['type'], typeMap[type(param)],
                             msg='Unexpected control type for %s' % tokenName)

    def test_on_mod_settings_changed_updates_config_file(self):
        from distancemarker.support.mods_settings_api_support import onModSettingsChanged, modLinkage
        from distancemarker.settings.config_file import g_configFiles
        from distancemarker.settings.config import g_config
        with temp_cwd() as tmpDir:
            g_config.reloadSafely()
            onModSettingsChanged(modLinkage, {'text-size': 12, 'mod-language': 1, 'text-color': 'FF0B00'})
            configDict = g_configFiles.config.loadConfigDict()
            self.assertEqual(configDict['text-size'], 12)
            self.assertEqual(configDict['mod-language'], u'de')
            self.assertEqual(configDict['text-color'], [255, 11, 0])
            self.assertEqual(configDict['near-distance-color'], [0, 153, 255])
            self.assertEqual(configDict['__version__'], 5)
            self.assertEqual(g_configParams.textSize.value, 12)
            self.assertEqual(g_configParams.modLanguage.value, 'de')

    def test_on_mod_settings_changed_ignores_foreign_linkage(self):
        from distancemarker.support.mods_settings_api_support import onModSettingsChanged
        from distancemarker.settings.config_file import g_configFiles
        from distancemarker.settings.config import g_config
        with temp_cwd() as tmpDir:
            g_config.reloadSafely()
            before = g_configFiles.config.loadConfigDict()
            onModSettingsChanged('some.other.mod', {'text-size': 12})
            after = g_configFiles.config.loadConfigDict()
            self.assertEqual(before, after)
