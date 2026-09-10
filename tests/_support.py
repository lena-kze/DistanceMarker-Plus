import os
import sys
import shutil
import tempfile
from contextlib import contextmanager

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
STUBS_DIR = os.path.join(TESTS_DIR, 'stubs')
SRC_DIR = os.path.join(PROJECT_ROOT, 'src', 'decompiled')
TRANSLATIONS_DIR = os.path.join(PROJECT_ROOT, 'modified', 'zip', 'res', 'gui', 'distancemarker', 'translations')
INTERIM_SWF = os.path.join(PROJECT_ROOT, 'interim', 'res', 'gui', 'flash', 'DistanceMarkerFlash.swf')
CONFIG_AS = os.path.join(PROJECT_ROOT, 'modified', 'scripts', 'com', 'github', 'pruszko', 'distancemarker', 'config', 'Config.as')
DISTANCE_MARKER_AS = os.path.join(PROJECT_ROOT, 'modified', 'scripts', 'com', 'github', 'pruszko', 'distancemarker', 'markers', 'DistanceMarker.as')

for _path in (STUBS_DIR, TESTS_DIR, SRC_DIR):
    if _path not in sys.path:
        sys.path.insert(0, _path)

from distancemarker.settings import translations
translations.loadTranslations()


def set_client_language(language):
    import helpers
    helpers._client_language = language


def set_language(language):
    set_client_language(language)
    from distancemarker.settings import translations
    translations.loadTranslations()


def reset_params():
    from distancemarker.settings.config_param import g_configParams
    for tokenName, param in g_configParams.items():
        param.value = param.defaultValue


def set_param(tokenName, value):
    from distancemarker.settings.config_param import g_configParams
    for paramTokenName, param in g_configParams.items():
        if paramTokenName == tokenName:
            param.value = value
            return param
    raise KeyError('No param registered for token %s' % tokenName)


def set_msa_present(enabled):
    from distancemarker import g_distanceMarkerMod
    from gui import modsSettingsApi
    g_distanceMarkerMod._DistanceMarkerMod__isModsSettingsApiPresent = bool(enabled)
    modsSettingsApi.g_modsSettingsApi = modsSettingsApi.msa_fake if enabled else None


@contextmanager
def temp_cwd():
    oldCwd = os.getcwd()
    tmpDir = tempfile.mkdtemp(prefix='distancemarker_tests_')
    os.chdir(tmpDir)
    try:
        yield tmpDir
    finally:
        os.chdir(oldCwd)
        shutil.rmtree(tmpDir, ignore_errors=True)