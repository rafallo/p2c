# -*- coding: utf-8 -*-
from PyQt5 import QtGui, QtCore, QtQuick
from PyQt5.QtCore import QUrl, QTimer
from gui.qml.classes import Tile
from gui.qml.deferred import SetMoviesThread, SearchThread
from p2c.app import P2CDaemon
from torrent.movie import Movie
from torrent.torrent import Torrent


class P2CQMLApplication(QtGui.QGuiApplication):
    def __init__(self, list_of_str):
        super().__init__(list_of_str)
        self._current_category = None
        self._current_torrent = None
        self._current_torrent_info = None
        self._status_timer = QTimer(self)
        self._movies_thread = None
        self._search_thread = None

    def run_view(self):
        self._view = QtQuick.QQuickView()
        self._rctx = self._view.rootContext()
        self._view.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)

        # set context variables
        self.categories = []
        self._rctx.setContextProperty("categoriesModel", self.categories)
        self.tiles = []
        self.torrents = []
        self._rctx.setContextProperty("moviesModel", self.tiles)
        self._set_loading(False)

        self._view.setSource(QtCore.QUrl('qml.qml'))
        #        self._view.showFullScreen()
        self._view.show()

    def connect_daemon(self, daemon: P2CDaemon):
        self._daemon = daemon
        self._set_categories()
        self._connect_signals()

    def play(self, movie: Movie):
        self._set_movie_status("Ready to play!")
        self._set_media(movie)
        self._daemon.play(movie)
        self._set_additional_media_info()

    def buffer(self, movie: Movie):
        seconds = self._current_torrent.get_seconds_to_buffer()
        info = "just started"
        if seconds:
            if seconds < 15:
                info = "just a moment"
            else:
                # rount to minutes
                minutes = int(seconds / 60) + 1
                if minutes == 1:
                    info = "1 minute"
                else:
                    info = "{} minutes".format(minutes)
        self._set_movie_status("Buffering... ({})".format(info))
        self._daemon.buffer(movie)
        self._set_additional_media_info()

    def wait_for_metadata(self):
        self._set_movie_status("Getting metadata...")
        if self._current_torrent:
            self._set_additional_media_info(self._current_torrent.name)

    def select_movie(self, torrent: Torrent) -> Movie:
        movies = torrent.get_movies()
        # TODO: show dialog with movie selecting instead of doing it automatically
        return max(movies, key=lambda x: x.size)

    def update_status(self):
        torrent = self._current_torrent
        if torrent:
            if(torrent.has_torrent_info()):
                movie = self.select_movie(torrent)
                torrent.download_file(movie.path)
                self._set_duration(movie)
                if not self._daemon.is_playing(movie):
                    if(movie.can_play()):
                        self.play(movie)
                    else:
                        self.buffer(movie)

                ### DEBUG INFO
                text = "s: %s, num p: %s, rate: %s kbs" % (
                    torrent.get_status()['state'],
                    torrent.get_status()['num_peers'],
                    int(torrent.get_status()['download_rate'] /1024),
                )
                self._view.rootObject().setProperty("debugText", text)
                ### END DEBUG INFO

            else:
                self.wait_for_metadata()
        else:
            self.wait_for_metadata()

    def on_category_clicked(self, index):
        # clear list
        self._set_torrents([], loading=True)

        category = self._daemon.get_categories()[index]
        self._current_category = category

        if self._current_category:
            self._search_thread = None
            self._movies_thread = SetMoviesThread(self._current_category)
            self._movies_thread.start()
            self._movies_thread.got_movies.connect(self._threaded_set_torrents)


    def on_movie_clicked(self, index):
        self._view.rootObject().setProperty("isMovieScene", True)

        torrent_ui = self.torrents[index]
        self._current_torrent = self._daemon.get_torrent(torrent_ui)
        self._current_torrent_info = torrent_ui
        self.update_status()

    def on_search(self, query):
        if len(query) < 3:
            return
            # clear list
        self._set_torrents([],loading=True)

        self._movies_thread = None
        self._search_thread = SearchThread(query, self._daemon.search)
        self._search_thread.start()
        self._search_thread.got_movies.connect(self._threaded_set_torrents)

    def on_exit(self):
        self.quit()

    def _connect_signals(self):
        self._view.rootObject().categoryClicked.connect(
            self.on_category_clicked)
        self._view.rootObject().movieClicked.connect(self.on_movie_clicked)
        self._view.rootObject().movieClicked.connect(self.on_movie_clicked)
        self._view.rootObject().searchQuery.connect(self.on_search)
        self._view.rootObject().exitAction.connect(self.on_exit)
        self._status_timer.timeout.connect(self.update_status)
        self._status_timer.start(500)

    def _set_movie_status(self, text):
        self._rctx.setContextProperty("movieStatus", text)

    def _set_media(self, movie: Movie):
        file_name = movie.get_target_path()
        self._rctx.setContextProperty("movieSource",
            QUrl.fromLocalFile(file_name))

    def _set_additional_media_info(self, title=None):
        self._rctx.setContextProperty("title",
            title or self._current_torrent_info.title or self._current_torrent_info.label)
        self._rctx.setContextProperty("poster",
            self._current_torrent_info.poster if self._current_torrent_info  and self._current_torrent_info.poster else '')

    def _set_categories(self):
        data = []
        for category in self._daemon.get_categories():
            data.append(Tile(category.label, category.service.name))
        self._rctx.setContextProperty("categoriesModel", data)
        self.categories = data

    def _threaded_set_torrents(self, data, thread):
        # if latest action
        if thread == self._movies_thread or thread == self._search_thread:
            self._set_torrents(data)

    def _set_torrents(self, data, loading=False):
        # only existing tiles
        for (tile, torrent_info) in zip(self.tiles, data[:len(self.tiles)]):
            if torrent_info.title:
                tile.name = torrent_info.title
                tile.source = torrent_info.label
            else:
                tile.name = torrent_info.label
                tile.source = None
            tile.poster = torrent_info.poster
            tile.description = torrent_info.description

        if len(data) != len(self.tiles):
            for torrent_info in data[len(self.tiles):]:
                if torrent_info.title:
                    tile = Tile(torrent_info.title, torrent_info.label,
                        torrent_info.poster, torrent_info.description)
                else:
                    tile = Tile(torrent_info.label, None, torrent_info.poster,
                        torrent_info.description)
                self.tiles.append(tile)

            self._rctx.setContextProperty("moviesModel", self.tiles)
        self.torrents = data
        self._set_loading(loading)

    def _set_loading(self, loading):
        self._rctx.setContextProperty("loadingMask", loading)

    def _set_duration(self, movie:Movie):
        tdelta = movie.get_movie_duration()
        if tdelta:
            self._view.rootObject().setProperty("movieDuration", tdelta.seconds * 1000)
