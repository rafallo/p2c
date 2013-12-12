# -*- coding: utf-8 -*-
import mimetypes
import threading
import logging
import os
import signal

from PyQt5.QtCore import QSettings, QTimer
from PyQt5.QtWidgets import QMainWindow, QTreeWidgetItem, QListWidgetItem, QLabel
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaResource, QMediaPlaylist

from p2c.app import Application
from gui.desktop.ui_mainwindow import Ui_MainWindow
from torrent.movie import Movie

logger = logging.getLogger("p2c")

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
        if self.media_player is None:
            self.media_player = QMediaPlayer(self.videoArea,
                QMediaPlayer.VideoSurface)
            self.media_player.setVideoOutput(self.videoArea.videoSurface())
        file_name = movie.get_target_path()
        mimetype = mimetypes.guess_type(file_name)[0]
        logger.debug("Found mimetype: {}".format(mimetype))
        media_res = QMediaResource(QUrl.fromLocalFile(file_name), mimetype)
        media = QMediaContent(media_res)
        self.media_player.setMedia(media)
        self.media_player.play()

    def connect_app(self, app: Application):
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
            if torrent.has_torrent_info():
                movie = torrent.get_downloading_movie()
                if movie:
                    data['movie'] = movie.name
                    data['movie progress'] = "{0:.2f}%".format(movie.progress * 100)
                    data['can_play'] = movie.can_play()
                data.update(torrent.get_status())
                data['progress'] = "{0:.2f}%".format(data['progress'] * 100)
                data['download_rate'] = "{0:.2f} kb/s".format(data['download_rate']/1000)
            else:
                data['status'] = "Getting metadata"
            text = "\n".join(["{}: {}".format(k,data[k]) for k in data])
        else:
            text="select item"
        self.statusArea.setText(text)

#        self.statusbar.removeWidget(self.statusbarWidget)
#        if(torrent.has_torrent_info()):
#            self.statusbarWidget = QLabel("Downloading...")
#        else:
#            self.statusbarWidget = QLabel("Getting metadata...")
#        self.statusbar.addWidget(self.statusbarWidget)

    def run_torrent(self, item):
        index = self.itemList.currentIndex()
        torrent_ui = self.current_category.get_torrents()[index.row()]
        torrent = self.app.get_torrent(torrent_ui)
        if(torrent.has_torrent_info()):
            movies = torrent.get_movies()
            #                        if (len(movies) == 1):
            #                print("playing %s" % movies[0])
            #            else:
            #                print(len(movies))
            # DEVELOPMENT
            movie = max(movies, key=lambda x:x.size)
            print(movie.size)
            torrent.download_file(movie.path)
            print(movie.can_play())
            if(movie.can_play()):
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

    def _connect_signals(self):
        self.menuTree.currentItemChanged.connect(self.change_category)
        self.itemList.currentItemChanged.connect(self.activate_torrent)
        self.itemList.itemDoubleClicked.connect(self.run_torrent)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(500)



