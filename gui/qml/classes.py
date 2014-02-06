# -*- coding: utf-8 -*-
from PyQt5 import QtCore

class Tile(QtCore.QObject):
    nameChanged = QtCore.pyqtSignal()
    posterChanged = QtCore.pyqtSignal()
    sourcehanged = QtCore.pyqtSignal()

    @QtCore.pyqtProperty(str, notify=nameChanged)
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if self._name != name:
            self._name = name
            self.nameChanged.emit()

    @QtCore.pyqtProperty(str, notify=posterChanged)
    def poster(self):
        return self._poster

    @poster.setter
    def poster(self, poster):
        if self._poster != poster:
            self._poster = poster
            self.posterChanged.emit()

    @QtCore.pyqtProperty(str, notify=sourcehanged)
    def source(self):
        return self._source

    @source.setter
    def source(self, source):
        if self._source != source:
            self._source = source
            self.sourceChanged.emit()

    def __init__(self, name='', source='', poster=None, parent=None):
        super(Tile, self).__init__(parent)

        self._name = name
        self._poster = poster
        self._source = source

