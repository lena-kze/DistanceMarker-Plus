# uncompyle6 version 3.9.2
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.8.10 (tags/v3.8.10:3d8993a, May  3 2021, 11:48:03) [MSC v.1928 64 bit (AMD64)]
# Embedded file name: src\distancemarker\settings\config_param.py
# Compiled at: 2025-06-19 21:09:26
from distancemarker.settings.config_param_types import *
from distancemarker.settings.translations import Tr, LANGUAGE_MAP

class DisplayMode(object):
    ALWAYS = 'always'
    ON_ALT_PRESSED = 'on-alt-pressed'


class AnchorPosition(object):
    TANK_MARKER = 'tank-marker'
    TANK_CENTER = 'tank-center'
    TANK_BOTTOM = 'tank-bottom'


class MarkerTarget(object):
    ALLY_AND_ENEMY = 'ally-and-enemy'
    ONLY_ENEMY = 'only-enemy'


class ModLanguage(object):
    EN = 'en'
    DE = 'de'


class ImpreciseDisplayMode(object):
    ALWAYS_SYMBOL = 'always-symbol'
    EXCEPT_VIEW_RANGE = 'except-view-range'
    ALWAYS_NUMBERS = 'always-numbers'


class ConfigParams(object):

    def __init__(self):
        self.enabled = BooleanParam([
            'enabled'], defaultValue=True, disabledValue=False)
        self.modLanguage = OptionsParam([
            'mod-language'], [
            Option(ModLanguage.EN, 0, LANGUAGE_MAP[ModLanguage.EN]),
            Option(ModLanguage.DE, 1, LANGUAGE_MAP[ModLanguage.DE])], defaultValue=ModLanguage.DE)
        self.displayMode = OptionsParam([
            'display-mode'], [
            Option(DisplayMode.ALWAYS, 0, Tr.DISPLAY_MODE_OPTION_ALWAYS),
            Option(DisplayMode.ON_ALT_PRESSED, 1, Tr.DISPLAY_MODE_OPTION_ON_ALT_PRESSED)], defaultValue=DisplayMode.ALWAYS)
        self.markerTarget = OptionsParam([
            'marker-target'], [
            Option(MarkerTarget.ALLY_AND_ENEMY, 0, Tr.MARKER_TARGET_OPTION_ALLY_AND_ENEMY),
            Option(MarkerTarget.ONLY_ENEMY, 1, Tr.MARKER_TARGET_OPTION_ONLY_ENEMY)], defaultValue=MarkerTarget.ONLY_ENEMY)
        self.anchorPosition = OptionsParam([
            'anchor-position'], [
            Option(AnchorPosition.TANK_MARKER, 0, Tr.ANCHOR_POSITION_OPTION_TANK_MARKER),
            Option(AnchorPosition.TANK_CENTER, 1, Tr.ANCHOR_POSITION_OPTION_TANK_CENTER),
            Option(AnchorPosition.TANK_BOTTOM, 2, Tr.ANCHOR_POSITION_OPTION_TANK_BOTTOM)], defaultValue=AnchorPosition.TANK_BOTTOM)
        self.lockPositionOffsets = BooleanParam([
            'lock-position-offsets'], defaultValue=True)
        self.anchorHorizontalOffset = StepperParam([
            'anchor-horizontal-offset'], castFunction=int, minValue=-150, step=1, maxValue=150, defaultValue=0)
        self.anchorVerticalOffset = StepperParam([
            'anchor-vertical-offset'], castFunction=int, minValue=-150, step=1, maxValue=150, defaultValue=0)
        self.decimalPrecision = SliderParam([
            'decimal-precision'], castFunction=int, minValue=0, step=1, maxValue=3, defaultValue=0)
        self.textSize = SliderParam([
            'text-size'], castFunction=int, minValue=6, step=1, maxValue=24, defaultValue=11)
        self.textColor = ColorParam([
            'text-color'], defaultValue=(255, 11, 0))
        self.textAlpha = SliderParam([
            'text-alpha'], castFunction=float, minValue=0.0, step=0.01, maxValue=1.0, defaultValue=0.9)
        self.drawTextOutline = BooleanParam([
            'draw-text-outline'], defaultValue=True)
        self.drawTextShadow = BooleanParam([
            'draw-text-shadow'], defaultValue=False)
        self.drawDistanceUnit = BooleanParam([
            'draw-distance-unit'], defaultValue=False)
        self.nearDistanceColor = ColorParam([
            'near-distance-color'], defaultValue=(0, 153, 255))
        self.zone3DistanceColor = ColorParam([
            'zone3-distance-color'], defaultValue=(255, 11, 0))
        self.zone4DistanceColor = ColorParam([
            'zone4-distance-color'], defaultValue=(255, 11, 0))
        self.zone5DistanceColor = ColorParam([
            'zone5-distance-color'], defaultValue=(255, 11, 0))
        self.farDistanceColor = ColorParam([
            'far-distance-color'], defaultValue=(255, 229, 0))
        self.impreciseDisplayMode = OptionsParam([
            'imprecise-display-mode'], [
             Option(ImpreciseDisplayMode.ALWAYS_SYMBOL, 0, Tr.IMPRECISE_DISPLAY_MODE_OPTION_ALWAYS_SYMBOL),
             Option(ImpreciseDisplayMode.EXCEPT_VIEW_RANGE, 1, Tr.IMPRECISE_DISPLAY_MODE_OPTION_EXCEPT_VIEW_RANGE),
             Option(ImpreciseDisplayMode.ALWAYS_NUMBERS, 2, Tr.IMPRECISE_DISPLAY_MODE_OPTION_ALWAYS_NUMBERS)],
            defaultValue=ImpreciseDisplayMode.EXCEPT_VIEW_RANGE)
        self.sizeBonusZone1 = SliderParam([
            'size-bonus-zone1'], castFunction=int, minValue=0, step=1, maxValue=25, defaultValue=7)
        self.sizeBonusZone2 = SliderParam([
            'size-bonus-zone2'], castFunction=int, minValue=0, step=1, maxValue=25, defaultValue=5)
        self.sizeBonusZone3 = SliderParam([
            'size-bonus-zone3'], castFunction=int, minValue=0, step=1, maxValue=25, defaultValue=4)
        self.sizeBonusZone4 = SliderParam([
            'size-bonus-zone4'], castFunction=int, minValue=0, step=1, maxValue=25, defaultValue=3)
        self.sizeBonusZone5 = SliderParam([
            'size-bonus-zone5'], castFunction=int, minValue=0, step=1, maxValue=25, defaultValue=2)
        self.sizeBonusZone6 = SliderParam([
            'size-bonus-zone6'], castFunction=int, minValue=0, step=1, maxValue=25, defaultValue=0)

    @staticmethod
    def items():
        return PARAM_REGISTRY.items()


g_configParams = ConfigParams()
