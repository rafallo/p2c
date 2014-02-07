# -*- coding: utf-8 -*-
from PyQt5 import QtGui, QtCore, QtQuick
from PyQt5.QtCore import QUrl, QTimer
from gui.qml.classes import Tile
from gui.qml.deferred import SetMoviesThread
from p2c.app import P2CDaemon
from p2c.ui import TorrentInfo
from torrent.movie import Movie
from torrent.torrent import Torrent


class P2CQMLApplication(QtGui.QGuiApplication):
    def __init__(self, list_of_str):
        super().__init__(list_of_str)
        self._current_category = None
        self._current_torrent = None
        self._status_timer = QTimer(self)
        self._movies_thread = None

    def run_view(self):
        self._view = QtQuick.QQuickView()
        self._rctx = self._view.rootContext()
        self._view.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)

        # set context variables
        self.categories = []
        self.movies = []
        self._rctx.setContextProperty("categoriesModel", self.categories)
        self.movies = []
        self._rctx.setContextProperty("moviesModel", self.movies)


        self._view.setSource(QtCore.QUrl('qml.qml'))
#        self.view.showFullScreen()
        self._view.show()

    def connect_daemon(self, daemon: P2CDaemon):
        self._daemon = daemon
        self._set_categories()
        self._connect_signals()

    def play(self, movie: Movie):
        self._set_movie_status("Ready to play!")
        self._set_media(movie)
        self._daemon.play(movie)

    def buffer(self, movie: Movie):
        self._set_movie_status("Buffering...")
        self._daemon.buffer(movie)

    def wait_for_metadata(self):
        self._set_movie_status("Getting metadata...")

    def select_movie(self, torrent: Torrent):
        movies = torrent.get_movies()
        # TODO: show dialog with movie selecting instead of doing it automatically
        return max(movies, key=lambda x: x.size)

    def update_status(self):
        torrent = self._current_torrent
        if torrent:
            if(torrent.has_torrent_info()):
                movie = self.select_movie(torrent)
                torrent.download_file(movie.path)
                if not self._daemon.is_playing(movie):
                    if(movie.can_play()):
                        self.play(movie)
                    else:
                        self.buffer(movie)
            else:
                self.wait_for_metadata()

        return
        if self.current_torrent:
            torrent = self.current_torrent
            if torrent and torrent.has_torrent_info():
                movie = torrent.get_downloading_movie()
                if movie:
                    data['movie'] = movie.name
                    if self.media_player:
                        self.positionSlider.setBackgroundValue(movie.progress * self.media_player.duration())
                    data['movie progress'] = "{0:.2f}%".format(movie.progress * 100)
                    data['can_play'] = movie.can_play()
                data.update(torrent.get_status())
                # TODO: buggy due to setting priority to 0
                if data['state'] == 'downloading':
                    del data['progress']
                else:
                    data['progress'] = "{0:.2f}%".format(data['progress'] * 100)
                data['download_rate'] = "{0:.2f} kb/s".format(data['download_rate']/1000)
            else:
                data['status'] = "Getting metadata"
            text = "\n".join(["{}: {}".format(k,data[k]) for k in data])

    def on_category_clicked(self, index):
        # clear list
        self._set_torrents([], self._current_category)

        category = self._daemon.get_categories()[index]
        self._current_category = category

        if self._current_category:
            self._movies_thread = SetMoviesThread(self._current_category, self._rctx)
            self._movies_thread.start()
            self._movies_thread.got_movies.connect(self._set_torrents)


    def on_movie_clicked(self, index):
        self._view.rootObject().setProperty("isMovieScene", True)

        torrent_ui = self._current_category.get_torrents(limit=20)[index]
        self._current_torrent = self._daemon.get_torrent(torrent_ui)
        self.update_status()

    def _connect_signals(self):
        self._view.rootObject().categoryClicked.connect(self.on_category_clicked)
        self._view.rootObject().movieClicked.connect(self.on_movie_clicked)
        self._status_timer.timeout.connect(self.update_status)
        self._status_timer.start(500)

    def _set_movie_status(self, text):
        self._rctx.setContextProperty("movieStatus", text)

    def _set_media(self, movie: Movie):
       file_name = movie.get_target_path()
       self._rctx.setContextProperty("movieSource", QUrl.fromLocalFile(file_name))

    def _set_categories(self):
        data = []
        for category in self._daemon.get_categories():
            data.append(Tile(category.label, category.service.name))
        self._rctx.setContextProperty("categoriesModel", data)
        self.categories = data

    def _set_torrents(self, data, category):
        if category == self._current_category:
            # only existing tiles
            for (tile, (movie,source,poster)) in zip(self.movies, data[:len(self.movies)]):
                tile.name = movie
                tile.source = source
                tile.poster = poster

            if len(data) != len(self.movies):
                for movie, source, poster in data[len(self.movies):]:
                    self.movies.append(Tile(movie, source, poster))

                self._rctx.setContextProperty("moviesModel", self.movies)
