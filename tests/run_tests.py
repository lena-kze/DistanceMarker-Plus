#!/usr/bin/env python
import os
import sys
import unittest
import zipfile

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_DIR = os.path.join(PROJECT_ROOT, 'tests')
for path in (PROJECT_ROOT, TESTS_DIR):
    if path not in sys.path:
        sys.path.insert(0, path)


def _ensure_swf_fixture():
    swf_path = os.path.join(PROJECT_ROOT, 'interim', 'res', 'gui', 'flash',
                            'DistanceMarkerFlash.swf')
    if os.path.isfile(swf_path):
        return
    candidates = [
        os.path.join(PROJECT_ROOT, 'build', 'DistanceMarker-Plus_2.3.0.wotmod'),
        os.path.join(PROJECT_ROOT, 'src', 'DistanceMarker-Plus_2.3.0.wotmod'),
    ]
    archive_path = next((path for path in candidates if os.path.isfile(path)), None)
    if archive_path is None:
        return
    with zipfile.ZipFile(archive_path, 'r') as archive:
        data = archive.read('res/gui/flash/DistanceMarkerFlash.swf')
    parent = os.path.dirname(swf_path)
    if not os.path.isdir(parent):
        os.makedirs(parent)
    with open(swf_path, 'wb') as swf_file:
        swf_file.write(data)


_ensure_swf_fixture()
import _support

from tests import (
    test_translations,
    test_config_params,
    test_config_template,
    test_migrations,
    test_config,
    test_settings_page,
    test_flash_serialization,
    test_actionscript,
)


def main():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for module in (
        test_translations,
        test_config_params,
        test_config_template,
        test_migrations,
        test_config,
        test_settings_page,
        test_flash_serialization,
        test_actionscript,
    ):
        suite.addTests(loader.loadTestsFromModule(module))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(main())
