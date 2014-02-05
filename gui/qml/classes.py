# -*- coding: utf-8 -*-
from PyQt5 import QtCore

class Tile(QtCore.QObject):
    nameChanged = QtCore.pyqtSignal()
    coverChanged = QtCore.pyqtSignal()
    sourcehanged = QtCore.pyqtSignal()

    @QtCore.pyqtProperty(str, notify=nameChanged)
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if self._name != name:
            self._name = name
            self.nameChanged.emit()

#    @QtCore.pyqtProperty(str, notify=coverChanged)
#    def cover(self):
#        return self._cover
#
#    @cover.setter
#    def cover(self, cover):
#        if self._cover != cover:
#            self._cover = cover
#            self.coverChanged.emit()

    @QtCore.pyqtProperty(str, notify=sourcehanged)
    def source(self):
        return self._source

    @source.setter
    def source(self, source):
        if self._source != source:
            self._source = source
            self.sourceChanged.emit()

    def __init__(self, name='', source='', parent=None):
        super(Tile, self).__init__(parent)

        self._name = name
        #        self._cover = cover
        self._source = source

