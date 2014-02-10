# -*- coding: utf-8 -*-
from threading import Thread
from PyQt5 import QtCore
from PyQt5.QtCore import QThread
from p2c.ui import CategoryInfo

class SetMoviesThread(QThread):
    got_movies = QtCore.pyqtSignal(list, CategoryInfo)

    def __init__(self, category, ctx, QObject_parent=None):
        super().__init__(QObject_parent)
        self.category = category
        self.ctx = ctx

        self.threads = []

    def run(self):
        self.data = []
        self.items = self.category.get_torrents(limit=32)
        self._process_no_posters()
        self._process_with_posters()

    def _process_no_posters(self):
        for torrent_info in self.items:
            data = {}
            th = Thread(target=self._get_additional_info,
                args=[torrent_info, data])
            self.threads.append((th, data))
            th.start()
            self.data.append((torrent_info.label, '', None, None))
        self.got_movies.emit(self.data, self.category)

    def _process_with_posters(self):
        updated_data = []
        for th, data in self.threads:
            th.join()
            if 'verbose_title' in data:
                updated_data.append(
                    (data['verbose_title'], data['title'],
                     data.get('poster', None), data['description']))
            else:
                updated_data.append(
                    (data['title'], '', data.get('poster', None),
                     data.get('description', None)))
        self.data[:] = updated_data
        self.got_movies.emit(self.data, self.category)

    def _get_additional_info(self, torrent_info, data):
        if torrent_info.get_poster():
            data['poster'] = torrent_info.get_poster()
        if torrent_info.get_description():
            data['description'] = torrent_info.get_description()
        if torrent_info.get_verbose_title():
            data['verbose_title'] = torrent_info.get_verbose_title()
        data['title'] = torrent_info.label