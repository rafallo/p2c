# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from PyQt5.QtCore import QThread

class SetMoviesThread(QThread):
    got_movies = QtCore.pyqtSignal(list)

    def __init__(self, category, ctx, QObject_parent=None):
        super().__init__(QObject_parent)
        self.category = category
        self.ctx = ctx


    def run(self):
        if self.category:
            items = map(lambda x: x.label,
                self.category.get_torrents(limit=20))
            self.data = []

            for movie in items:
                self.data.append((movie, self.category.service.name))
            self.got_movies.emit(self.data)
