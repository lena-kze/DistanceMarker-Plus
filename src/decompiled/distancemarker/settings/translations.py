# uncompyle6 version 3.9.2
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.8.10 (tags/v3.8.10:3d8993a, May  3 2021, 11:48:03) [MSC v.1928 64 bit (AMD64)]
# Embedded file name: src\distancemarker\settings\translations.py
# Compiled at: 2025-06-19 21:20:34
import json, logging, ResMgr
from helpers import getClientLanguage
logger = logging.getLogger(__name__)
DEBUG_LANGUAGE = None
DEFAULT_TRANSLATIONS_MAP = {}
TRANSLATIONS_MAP = {}
CURRENT_LANGUAGE = 'en'
LANGUAGE_MAP = {'en': 'Englisch', 'de': 'Deutsch'}
AVAILABLE_LANGUAGES = ['en', 'de']

def _clearTrCache():
    for translationDescriptor in Tr.__dict__.values():
        if isinstance(translationDescriptor, TranslationBase):
            translationDescriptor._value = None


def loadTranslations():
    global DEFAULT_TRANSLATIONS_MAP
    global TRANSLATIONS_MAP
    global CURRENT_LANGUAGE
    defaultTranslationsMap = _loadLanguage('en')
    DEFAULT_TRANSLATIONS_MAP = defaultTranslationsMap if defaultTranslationsMap is not None else {}
    if DEBUG_LANGUAGE is not None:
        language = DEBUG_LANGUAGE
        logger.info('Client language (debug): %s', language)
    else:
        language = getClientLanguage()
        logger.info('Client language: %s', language)
    if language not in AVAILABLE_LANGUAGES:
        logger.info('Translations for language %s not available, fallback to en' % language)
        language = 'en'
    CURRENT_LANGUAGE = language
    translationsMap = _loadLanguage(language)
    if translationsMap is not None:
        logger.info('Translations for language %s detected' % language)
        TRANSLATIONS_MAP = translationsMap
    else:
        logger.info('Translations for language %s not present, fallback to en' % language)
        TRANSLATIONS_MAP = {}
    _clearTrCache()
    return


def reloadTranslations(language):
    global DEFAULT_TRANSLATIONS_MAP
    global TRANSLATIONS_MAP
    global CURRENT_LANGUAGE
    if language not in AVAILABLE_LANGUAGES:
        logger.info('Language %s not available, fallback to en' % language)
        language = 'en'
    if language == CURRENT_LANGUAGE:
        return False
    logger.info('Reloading translations for language %s' % language)
    defaultTranslationsMap = _loadLanguage('en')
    DEFAULT_TRANSLATIONS_MAP = defaultTranslationsMap if defaultTranslationsMap is not None else {}
    translationsMap = _loadLanguage(language)
    if translationsMap is not None:
        logger.info('Translations for language %s detected' % language)
        TRANSLATIONS_MAP = translationsMap
    else:
        logger.info('Translations for language %s not present, fallback to en' % language)
        TRANSLATIONS_MAP = {}
    CURRENT_LANGUAGE = language
    _clearTrCache()
    return True


def _loadLanguage(language):
    translationsRes = ResMgr.openSection('gui/distancemarker/translations/translations_%s.json' % language)
    if translationsRes is None:
        return
    else:
        translationsStr = str(translationsRes.asBinary)
        return json.loads(translationsStr, encoding='UTF-8')


class TranslationBase(object):

    def __init__(self, tokenName):
        self._tokenName = tokenName
        self._value = None
        return

    def __get__(self, instance, owner=None):
        if self._value is None:
            self._value = self._generateTranslation()
        return self._value

    def _generateTranslation(self):
        raise NotImplementedError()


class TranslationElement(TranslationBase):

    def _generateTranslation(self):
        if self._tokenName in TRANSLATIONS_MAP:
            return TRANSLATIONS_MAP[self._tokenName]
        return DEFAULT_TRANSLATIONS_MAP[self._tokenName]


class TranslationList(TranslationBase):

    def _generateTranslation(self):
        if self._tokenName in TRANSLATIONS_MAP:
            return ('').join(TRANSLATIONS_MAP[self._tokenName])
        return ('').join(DEFAULT_TRANSLATIONS_MAP[self._tokenName])


class Tr(object):
    MODNAME = TranslationElement('modname')
    CHECKED = TranslationElement('checked')
    UNCHECKED = TranslationElement('unchecked')
    DEFAULT_VALUE = TranslationElement('defaultValue')
    INTRO_LABEL = TranslationElement('intro.label')
    INTRO_HEADER = TranslationElement('intro.header')
    INTRO_BODY = TranslationList('intro.body')
    INTRO_NOTE = TranslationList('intro.note')
    MOD_LANGUAGE_HEADER = TranslationElement('mod-language.header')
    MOD_LANGUAGE_BODY = TranslationList('mod-language.body')
    VISIBILITY_SETTINGS_LABEL = TranslationElement('visibility-settings.label')
    DISPLAY_MODE_HEADER = TranslationElement('display-mode.header')
    DISPLAY_MODE_BODY = TranslationList('display-mode.body')
    DISPLAY_MODE_OPTION_ALWAYS = TranslationElement('display-mode.option.always')
    DISPLAY_MODE_OPTION_ON_ALT_PRESSED = TranslationElement('display-mode.option.on-alt-pressed')
    MARKER_TARGET_HEADER = TranslationElement('marker-target.header')
    MARKER_TARGET_BODY = TranslationList('marker-target.body')
    MARKER_TARGET_OPTION_ALLY_AND_ENEMY = TranslationElement('marker-target.option.ally-and-enemy')
    MARKER_TARGET_OPTION_ONLY_ENEMY = TranslationElement('marker-target.option.only-enemy')
    POSITION_SETTINGS_LABEL = TranslationElement('position-settings.label')
    ANCHOR_POSITION_HEADER = TranslationElement('anchor-position.header')
    ANCHOR_POSITION_BODY = TranslationList('anchor-position.body')
    ANCHOR_POSITION_OPTION_TANK_MARKER = TranslationElement('anchor-position.option.tank-marker')
    ANCHOR_POSITION_OPTION_TANK_CENTER = TranslationElement('anchor-position.option.tank-center')
    ANCHOR_POSITION_OPTION_TANK_BOTTOM = TranslationElement('anchor-position.option.tank-bottom')
    LOCK_POSITION_OFFSETS_HEADER = TranslationElement('lock-position-offsets.header')
    LOCK_POSITION_OFFSETS_BODY = TranslationList('lock-position-offsets.body')
    ANCHOR_HORIZONTAL_OFFSET_HEADER = TranslationElement('anchor-horizontal-offset.header')
    ANCHOR_HORIZONTAL_OFFSET_BODY = TranslationList('anchor-horizontal-offset.body')
    ANCHOR_VERTICAL_OFFSET_HEADER = TranslationElement('anchor-vertical-offset.header')
    ANCHOR_VERTICAL_OFFSET_BODY = TranslationList('anchor-vertical-offset.body')
    VISUAL_SETTINGS_LABEL = TranslationElement('visual-settings.label')
    DECIMAL_PRECISION_HEADER = TranslationElement('decimal-precision.header')
    DECIMAL_PRECISION_BODY = TranslationList('decimal-precision.body')
    TEXT_SIZE_HEADER = TranslationElement('text-size.header')
    TEXT_SIZE_BODY = TranslationList('text-size.body')
    TEXT_ALPHA_HEADER = TranslationElement('text-alpha.header')
    TEXT_ALPHA_BODY = TranslationList('text-alpha.body')
    DRAW_TEXT_OUTLINE_HEADER = TranslationElement('draw-text-outline.header')
    DRAW_TEXT_OUTLINE_BODY = TranslationList('draw-text-outline.body')
    DRAW_TEXT_SHADOW_HEADER = TranslationElement('draw-text-shadow.header')
    DRAW_TEXT_SHADOW_BODY = TranslationList('draw-text-shadow.body')
    DRAW_DISTANCE_UNIT_HEADER = TranslationElement('draw-distance-unit.header')
    DRAW_DISTANCE_UNIT_BODY = TranslationList('draw-distance-unit.body')
    IMPRECISE_DISPLAY_MODE_HEADER = TranslationElement('imprecise-display-mode.header')
    IMPRECISE_DISPLAY_MODE_BODY = TranslationList('imprecise-display-mode.body')
    IMPRECISE_DISPLAY_MODE_OPTION_ALWAYS_SYMBOL = TranslationElement('imprecise-display-mode.option.always-symbol')
    IMPRECISE_DISPLAY_MODE_OPTION_EXCEPT_VIEW_RANGE = TranslationElement('imprecise-display-mode.option.except-view-range')
    IMPRECISE_DISPLAY_MODE_OPTION_ALWAYS_NUMBERS = TranslationElement('imprecise-display-mode.option.always-numbers')
    TEXT_COLOR_HEADER = TranslationElement('text-color.header')
    TEXT_COLOR_BODY = TranslationList('text-color.body')
    NEAR_DISTANCE_COLOR_HEADER = TranslationElement('near-distance-color.header')
    NEAR_DISTANCE_COLOR_BODY = TranslationList('near-distance-color.body')
    FAR_DISTANCE_COLOR_HEADER = TranslationElement('far-distance-color.header')
    FAR_DISTANCE_COLOR_BODY = TranslationList('far-distance-color.body')
    DISTANCE_ZONE_COLORS_LABEL = TranslationElement('distance-zone-colors.label')
    ZONE1_INFO_LABEL = TranslationElement('zone-1.info')
    ZONE2_INFO_LABEL = TranslationElement('zone-2.info')
    ZONE3_INFO_LABEL = TranslationElement('zone-3.info')
    ZONE4_INFO_LABEL = TranslationElement('zone-4.info')
    ZONE5_INFO_LABEL = TranslationElement('zone-5.info')
    ZONE6_INFO_LABEL = TranslationElement('zone-6.info')
    FOOTER_LABEL = TranslationElement('footer.label')
    ZONE3_DISTANCE_COLOR_HEADER = TranslationElement('zone3-distance-color.header')
    ZONE3_DISTANCE_COLOR_BODY = TranslationList('zone3-distance-color.body')
    ZONE4_DISTANCE_COLOR_HEADER = TranslationElement('zone4-distance-color.header')
    ZONE4_DISTANCE_COLOR_BODY = TranslationList('zone4-distance-color.body')
    ZONE5_DISTANCE_COLOR_HEADER = TranslationElement('zone5-distance-color.header')
    ZONE5_DISTANCE_COLOR_BODY = TranslationList('zone5-distance-color.body')
    SIZE_BONUS_ZONE1_HEADER = TranslationElement('size-bonus-zone1.header')
    SIZE_BONUS_ZONE1_BODY = TranslationList('size-bonus-zone1.body')
    SIZE_BONUS_ZONE2_HEADER = TranslationElement('size-bonus-zone2.header')
    SIZE_BONUS_ZONE2_BODY = TranslationList('size-bonus-zone2.body')
    SIZE_BONUS_ZONE3_HEADER = TranslationElement('size-bonus-zone3.header')
    SIZE_BONUS_ZONE3_BODY = TranslationList('size-bonus-zone3.body')
    SIZE_BONUS_ZONE4_HEADER = TranslationElement('size-bonus-zone4.header')
    SIZE_BONUS_ZONE4_BODY = TranslationList('size-bonus-zone4.body')
    SIZE_BONUS_ZONE5_HEADER = TranslationElement('size-bonus-zone5.header')
    SIZE_BONUS_ZONE5_BODY = TranslationList('size-bonus-zone5.body')
    SIZE_BONUS_ZONE6_HEADER = TranslationElement('size-bonus-zone6.header')
    SIZE_BONUS_ZONE6_BODY = TranslationList('size-bonus-zone6.body')
