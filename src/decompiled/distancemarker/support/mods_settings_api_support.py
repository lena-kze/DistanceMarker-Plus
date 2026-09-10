# uncompyle6 version 3.9.2
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.8.10 (tags/v3.8.10:3d8993a, May  3 2021, 11:48:03) [MSC v.1928 64 bit (AMD64)]
# Embedded file name: src\distancemarker\support\mods_settings_api_support.py
# Compiled at: 2025-06-19 21:21:02
import logging
from distancemarker.settings.translations import Tr
from distancemarker.settings.config import g_config
from distancemarker.settings.config_param import g_configParams, createTooltip
from distancemarker.utils import ObservingSemaphore
from gui.modsSettingsApi import g_modsSettingsApi
logger = logging.getLogger(__name__)
modLinkage = 'com.github.pruszko.distancemarker'

def registerSoftDependencySupport():
    template = {'modDisplayName': 'DistanceMarker-Plus', 
       'enabled': (g_configParams.enabled.defaultMsaValue), 
       'column1': (_createIntroPart() + _endSection() + _createVisibilitySettings() + _endSection() + _createPositionSettings()), 
       'column2': (_createVisualSettings() + _endSection() + _createUserSettings() + _createFooter())}
    g_modsSettingsApi.setModTemplate(modLinkage, template, onModSettingsChanged)


def refreshSettingsPage():
    try:
        registerSoftDependencySupport()
    except Exception:
        logger.error('Failed to refresh settings page.', exc_info=True)


settingsChangedSemaphore = ObservingSemaphore()

def onConfigFileReload():
    msaSettings = {}
    for tokenName, param in g_configParams.items():
        msaSettings[tokenName] = param.msaValue

    logger.info('Synchronizing config file -> ModsSettingsAPI')
    g_modsSettingsApi.updateModSettings(modLinkage, newSettings=msaSettings)


@settingsChangedSemaphore.withIgnoringLock(returnForIgnored=None)
def onModSettingsChanged(linkage, newSettings):
    if linkage != modLinkage:
        return
    try:
        serializedSettings = {}
        for tokenName, param in g_configParams.items():
            if tokenName not in newSettings:
                continue
            value = param.fromMsaValue(newSettings[tokenName])
            jsonValue = param.toJsonValue(value)
            serializedSettings[param.tokenName] = jsonValue

        logger.info('Synchronizing ModsSettingsAPI -> config file')
        g_config.updateConfigSafely(serializedSettings)
    except Exception:
        logger.error('Error occurred while ModsSettingsAPI settings change.', exc_info=True)


def _endSection():
    return _emptyLine(3)


def _innerSectionSeparator():
    return _emptyLine(4)


def _emptyLine(count=1):
    return [
     {'type': 'Empty'}] * count


def _createIntroPart():
    return [
     {'type': 'Label', 
        'text': (Tr.INTRO_LABEL), 
        'tooltip': (createTooltip(header=Tr.INTRO_HEADER, body=Tr.INTRO_BODY + '\n', note=Tr.INTRO_NOTE))}]


def _createLanguageSetting():
    return [g_configParams.modLanguage.renderParam(header=Tr.MOD_LANGUAGE_HEADER, body=Tr.MOD_LANGUAGE_BODY)]


def _createVisibilitySettings():
    return [{'type': 'Label', 'text': (Tr.VISIBILITY_SETTINGS_LABEL)}] + _emptyLine(2) + [
     g_configParams.displayMode.renderParam(header=Tr.DISPLAY_MODE_HEADER, body=Tr.DISPLAY_MODE_BODY),
     g_configParams.markerTarget.renderParam(header=Tr.MARKER_TARGET_HEADER, body=Tr.MARKER_TARGET_BODY)]


def _createPositionSettings():
    return [{'type': 'Label', 'text': (Tr.POSITION_SETTINGS_LABEL)}] + _emptyLine(2) + [
     g_configParams.anchorPosition.renderParam(header=Tr.ANCHOR_POSITION_HEADER, body=Tr.ANCHOR_POSITION_BODY),
     g_configParams.lockPositionOffsets.renderParam(header=Tr.LOCK_POSITION_OFFSETS_HEADER, body=Tr.LOCK_POSITION_OFFSETS_BODY),
     g_configParams.anchorHorizontalOffset.renderParam(header=Tr.ANCHOR_HORIZONTAL_OFFSET_HEADER, body=Tr.ANCHOR_HORIZONTAL_OFFSET_BODY),
     g_configParams.anchorVerticalOffset.renderParam(header=Tr.ANCHOR_VERTICAL_OFFSET_HEADER, body=Tr.ANCHOR_VERTICAL_OFFSET_BODY)]


def _createVisualSettings():
    return [{'type': 'Label', 'text': (Tr.VISUAL_SETTINGS_LABEL)}] + _emptyLine(2) + [
     g_configParams.decimalPrecision.renderParam(header=Tr.DECIMAL_PRECISION_HEADER, body=Tr.DECIMAL_PRECISION_BODY),
     g_configParams.textSize.renderParam(header=Tr.TEXT_SIZE_HEADER, body=Tr.TEXT_SIZE_BODY),
     g_configParams.textAlpha.renderParam(header=Tr.TEXT_ALPHA_HEADER, body=Tr.TEXT_ALPHA_BODY),
     g_configParams.drawTextOutline.renderParam(header=Tr.DRAW_TEXT_OUTLINE_HEADER, body=Tr.DRAW_TEXT_OUTLINE_BODY),
     g_configParams.drawTextShadow.renderParam(header=Tr.DRAW_TEXT_SHADOW_HEADER, body=Tr.DRAW_TEXT_SHADOW_BODY),
     g_configParams.drawDistanceUnit.renderParam(header=Tr.DRAW_DISTANCE_UNIT_HEADER, body=Tr.DRAW_DISTANCE_UNIT_BODY)]


def _createUserSettings():
    return [
     g_configParams.impreciseDisplayMode.renderParam(header=Tr.IMPRECISE_DISPLAY_MODE_HEADER, body=Tr.IMPRECISE_DISPLAY_MODE_BODY, showDefault=False)] + _innerSectionSeparator() + [
     {'type': 'Label', 'text': (Tr.DISTANCE_ZONE_COLORS_LABEL)}] + _emptyLine(2) + [
     {'type': 'Label', 'text': (Tr.ZONE1_INFO_LABEL)},
     g_configParams.nearDistanceColor.renderParam(header=Tr.NEAR_DISTANCE_COLOR_HEADER, body=Tr.NEAR_DISTANCE_COLOR_BODY),
     g_configParams.sizeBonusZone1.renderParam(header=Tr.SIZE_BONUS_ZONE1_HEADER, body=Tr.SIZE_BONUS_ZONE1_BODY),
     {'type': 'Label', 'text': (Tr.ZONE2_INFO_LABEL)},
     g_configParams.textColor.renderParam(header=Tr.TEXT_COLOR_HEADER, body=Tr.TEXT_COLOR_BODY),
     g_configParams.sizeBonusZone2.renderParam(header=Tr.SIZE_BONUS_ZONE2_HEADER, body=Tr.SIZE_BONUS_ZONE2_BODY),
     {'type': 'Label', 'text': (Tr.ZONE3_INFO_LABEL)},
     g_configParams.zone3DistanceColor.renderParam(header=Tr.ZONE3_DISTANCE_COLOR_HEADER, body=Tr.ZONE3_DISTANCE_COLOR_BODY),
     g_configParams.sizeBonusZone3.renderParam(header=Tr.SIZE_BONUS_ZONE3_HEADER, body=Tr.SIZE_BONUS_ZONE3_BODY),
     {'type': 'Label', 'text': (Tr.ZONE4_INFO_LABEL)},
     g_configParams.zone4DistanceColor.renderParam(header=Tr.ZONE4_DISTANCE_COLOR_HEADER, body=Tr.ZONE4_DISTANCE_COLOR_BODY),
     g_configParams.sizeBonusZone4.renderParam(header=Tr.SIZE_BONUS_ZONE4_HEADER, body=Tr.SIZE_BONUS_ZONE4_BODY),
     {'type': 'Label', 'text': (Tr.ZONE5_INFO_LABEL)},
     g_configParams.zone5DistanceColor.renderParam(header=Tr.ZONE5_DISTANCE_COLOR_HEADER, body=Tr.ZONE5_DISTANCE_COLOR_BODY),
      g_configParams.sizeBonusZone5.renderParam(header=Tr.SIZE_BONUS_ZONE5_HEADER, body=Tr.SIZE_BONUS_ZONE5_BODY),
      {'type': 'Label', 'text': (Tr.ZONE6_INFO_LABEL)},
      g_configParams.farDistanceColor.renderParam(header=Tr.FAR_DISTANCE_COLOR_HEADER, body=Tr.FAR_DISTANCE_COLOR_BODY),
      g_configParams.sizeBonusZone6.renderParam(header=Tr.SIZE_BONUS_ZONE6_HEADER, body=Tr.SIZE_BONUS_ZONE6_BODY)]


def _createFooter():
    return [{'type': 'Label', 'text': Tr.FOOTER_LABEL}]


def _createRainbowText(text):
    parts = []
    characterCount = len(text)
    for index, character in enumerate(text):
        color = _hueToHex(index / float(max(characterCount - 1, 1)))
        character = character.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        parts.append("<font color='%s'>%s</font>" % (color, character))
    return ''.join(parts)


def _hueToHex(fraction):
    hue = fraction * 360
    chroma = (1 - abs(2 * 0.55 - 1)) * 1.0
    scaledHue = hue / 60.0
    secondary = chroma * (1 - abs(scaledHue % 2 - 1))
    if scaledHue < 1:
        red, green, blue = chroma, secondary, 0
    elif scaledHue < 2:
        red, green, blue = secondary, chroma, 0
    elif scaledHue < 3:
        red, green, blue = 0, chroma, secondary
    elif scaledHue < 4:
        red, green, blue = 0, secondary, chroma
    elif scaledHue < 5:
        red, green, blue = secondary, 0, chroma
    else:
        red, green, blue = chroma, 0, secondary
    match = 0.55 - chroma / 2.0
    red = int(round((red + match) * 255))
    green = int(round((green + match) * 255))
    blue = int(round((blue + match) * 255))
    return '#%02x%02x%02x' % (red, green, blue)


def _createImg(src, width=None, height=None, vSpace=None, hSpace=None):
    template = "<img src='{0}' "
    absoluteUrl = 'img://gui/distancemarker/' + src
    if width is not None:
        template += "width='{1}' "
    if height is not None:
        template += "height='{2}' "
    if vSpace is not None:
        template += "vspace='{3}' "
    if hSpace is not None:
        template += "hspace='{4}'  "
    template += '/>'
    return template.format(absoluteUrl, width, height, vSpace, hSpace)
