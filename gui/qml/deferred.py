# -*- coding: utf-8 -*-
from threading import Thread
from PyQt5 import QtCore
from PyQt5.QtCore import QThread

class SetMoviesThread(QThread):
    got_movies = QtCore.pyqtSignal(list)

    def __init__(self, category, ctx, QObject_parent=None):
        super().__init__(QObject_parent)
        self.category = category
        self.ctx = ctx

        self.threads = []


    def run(self):
        items = self.category.get_torrents(limit=20)
        self.data = []

        for movie in items:
            data = {}
            th = Thread(target=self._get_additional_info, args=[movie, data])
            self.threads.append((th, data))
            th.start()

        for th, data in self.threads:
            th.join()
            self.data.append((data['verbose_title'], self.category.service.name, data['poster']))
        self.got_movies.emit(self.data)

    def _get_additional_info(self, movie, data):
        data['poster'] = movie.get_poster()
        data['verbose_title'] = movie.get_verbose_title()

