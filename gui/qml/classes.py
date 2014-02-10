# -*- coding: utf-8 -*-
from PyQt5 import QtCore

class Tile(QtCore.QObject):
    nameChanged = QtCore.pyqtSignal()
    posterChanged = QtCore.pyqtSignal()
    sourceChanged = QtCore.pyqtSignal()
    descriptionChanged = QtCore.pyqtSignal()

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

    @QtCore.pyqtProperty(str, notify=sourceChanged)
    def source(self):
        return self._source

    @source.setter
    def source(self, source):
        if self._source != source:
            self._source = source
            self.sourceChanged.emit()

    @QtCore.pyqtProperty(str, notify=descriptionChanged)
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        if self._description != description:
            self._description = description
            self.descriptionChanged.emit()

    def __init__(self, name='', source='', poster=None, description='',parent=None):
        super(Tile, self).__init__(parent)

        self._name = name
        self._poster = poster
        self._source = source
        self._description = description

