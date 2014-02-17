# -*- coding: utf-8 -*-
import mimetypes
import threading
import logging
import os
import signal

from PyQt5.QtCore import QSettings, QTimer
from PyQt5.QtWidgets import QMainWindow, QTreeWidgetItem, QListWidgetItem, QLabel, QStyle
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaResource

from p2c.app import P2CDaemon
from gui.desktop.ui_mainwindow import Ui_MainWindow
from torrent.movie import Movie

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow, Ui_MainWindow):
    settings = QSettings('Rafał Jagoda', 'Peer 2 cinema')
    settings.setFallbacksEnabled(False)
    version = '1.0'

    def __init__( self, parent=None ):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.media_player = None
        self.setWindowTitle('name of the software - ' + self.version)
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.show()
        self.timer = QTimer(self)

        self.current_category = None


    def play(self, movie: Movie):
        self.app.play(movie)
        self.media_player.play()
        self.playButton.setEnabled(True)

    def connect_app(self, app: P2CDaemon):
        self.app = app
        self._set_categories()
        self._connect_signals()

    def change_category(self, item):
        index = self.menuTree.indexOfTopLevelItem(item)
        category = self.app.get_categories()[index]
        self.current_category = category
        self.itemList.clear()
        threading.Thread(target=self._set_torrents).start()

    def activate_torrent(self, item):
        self.update_status()

    def update_status(self):
        index = self.itemList.currentIndex().row()
        if index != -1:
            data= {}
            torrent_ui = self.current_category.get_torrents()[index]
            torrent = self.app.get_torrent(torrent_ui)
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
        else:
            text="select item"
        self.statusArea.setText(text)

    def run_torrent(self, item):
        index = self.itemList.currentIndex()
        torrent_ui = self.current_category.get_torrents()[index.row()]
        torrent = self.app.get_torrent(torrent_ui)
        if(torrent.has_torrent_info()):
            movies = torrent.get_movies()
            # DEVELOPMENT

            movie = max(movies, key=lambda x:x.size)
            torrent.download_file(movie.path)

            if(movie.can_play()):
                self._set_media(movie)
                self.play(movie)
            else:
                self.app.buffer(movie)

    def _set_categories(self):
        for category in self.app.get_categories():
            item = QTreeWidgetItem(self.menuTree)
            item.setText(0, category.label)

    def _set_torrents(self):
        category = self.current_category
        items = map(lambda x: x.label,
            category.get_torrents(limit=20))
        # after long call
        if(self.current_category == category):
            self.itemList.addItems(list(items))

    def toggle_player(self):
       if self.media_player.state() == QMediaPlayer.PlayingState:
           self.media_player.pause()
       else:
           self.media_player.play()

    def set_player_position(self, position):
        self.media_player.setPosition(position)

    def media_state_changed(self, state):
        if state == QMediaPlayer.PlayingState:
            self.playButton.setIcon(self.videoArea.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(self.videoArea.style().standardIcon(QStyle.SP_MediaPlay))

    def position_changed(self, position):
        self.positionSlider.setValue(position)

    def duration_changed(self, duration):
        self.positionSlider.setRange(0, duration)

    def _connect_signals(self):
        self.menuTree.currentItemChanged.connect(self.change_category)
        self.itemList.currentItemChanged.connect(self.activate_torrent)
        self.itemList.itemDoubleClicked.connect(self.run_torrent)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(500)

    def _connect_player_signals(self):
        self.playButton.clicked.connect(self.toggle_player)
        self.positionSlider.sliderMoved.connect(self.set_player_position)
        self.media_player.stateChanged.connect(self.media_state_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.media_player.positionChanged.connect(self.position_changed)

    def _set_media(self, movie: Movie):
        if self.media_player is None:
            self.media_player = QMediaPlayer(self.videoArea,
                QMediaPlayer.VideoSurface)
            self.media_player.setVideoOutput(self.videoArea.videoSurface())
            self._connect_player_signals()
        file_name = movie.get_target_path()
        mimetype = mimetypes.guess_type(file_name)[0]
        logger.debug("Found mimetype: {}".format(mimetype))
        media_res = QMediaResource(QUrl.fromLocalFile(file_name), mimetype)
        media = QMediaContent(media_res)
        self.media_player.setMedia(media)