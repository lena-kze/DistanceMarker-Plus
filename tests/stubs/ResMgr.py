import os

from _support import TRANSLATIONS_DIR


class Section(object):

    def __init__(self, data):
        self._data = data

    @property
    def asBinary(self):
        return self._data


def openSection(virtualPath):
    translationsPrefix = 'gui/distancemarker/translations/'
    if not virtualPath.startswith(translationsPrefix):
        return None
    realPath = os.path.join(TRANSLATIONS_DIR, os.path.basename(virtualPath))
    if not os.path.isfile(realPath):
        return None
    with open(realPath, 'rb') as sectionFile:
        return Section(sectionFile.read())