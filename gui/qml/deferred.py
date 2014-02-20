# -*- coding: utf-8 -*-
from threading import Thread
from PyQt5 import QtCore
from PyQt5.QtCore import QThread


class AbstractMoviesThread(QThread):
    got_movies = QtCore.pyqtSignal(list, QThread)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.threads = []

    def get_torrents(self):
        raise NotImplementedError

    def run(self):
        self.data = []
        self.items = self.get_torrents()
        self._process_no_posters()
        self._process_with_posters()

    def _process_no_posters(self):
        for torrent_info in self.items:
            th = Thread(target=torrent_info.get_additional_info)
            self.threads.append(th)
            th.start()
        self.got_movies.emit(self.items, self)

    def _process_with_posters(self):
        for th in self.threads:
            th.join()
        self.got_movies.emit(self.items, self)


class SetMoviesThread(AbstractMoviesThread):
    def __init__(self, category, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category = category

    def get_torrents(self):
        dd = self.category.get_torrents(limit=32)
        return dd

class SearchThread(AbstractMoviesThread):
    def __init__(self, query, search_fun, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.query = query
        self.search_fun = search_fun

    def get_torrents(self):
        return self.search_fun(self.query)