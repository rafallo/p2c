# -*- coding: utf-8 -*-
from PyQt5 import QtGui, QtCore, QtQuick
from PyQt5.QtCore import QUrl
from gui.qml.classes import Tile
from gui.qml.deferred import SetMoviesThread
from p2c.app import Application


class QMLBinding(QtGui.QGuiApplication):
    def __init__(self, list_of_str):
        super().__init__(list_of_str)
        self.current_category = None

    def run_view(self):
        self.view = QtQuick.QQuickView()
        self.ctx = self.view.rootContext()
        self.view.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)
        self.categories = []
        self.ctx.setContextProperty("categoriesModel", self.categories)
        self.movies = []
        self.ctx.setContextProperty("moviesModel", self.movies)

        self.view.setSource(QtCore.QUrl('qml.qml'))

        self.view.show()

    def connect_app(self, app: Application):
        self.app = app
        self._set_categories()
        self._connect_signals()



    def on_category_clicked(self, index):
        # clear list
        self._set_torrents([])

        category = self.app.get_categories()[index]
        self.current_category = category

        self.thread = SetMoviesThread(self.current_category, self.ctx)
        self.thread.start()
        self.thread.got_movies.connect(self._set_torrents)

    def _connect_signals(self):
        self.view.rootObject().categoryClicked.connect(self.on_category_clicked)

    def _set_categories(self):
        data = []
        for category in self.app.get_categories():
            data.append(Tile(category.label, category.service.name))
        self.ctx.setContextProperty("categoriesModel", data)
        self.categories = data


    def _set_torrents(self, data):
        tiles = []
        for movie, source in data:
            tiles.append(Tile(movie, source))
        self.ctx.setContextProperty("moviesModel", tiles)
        self.movies = tiles

