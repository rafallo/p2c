# -*- coding: utf-8 -*-
import os
import logging
from urllib.parse import urlparse
import urllib.request
from p2c import settings
from torrent.torrent import TorrentObject
from p2c.ui import Torrent
from torrent.movie import Movie

logger = logging.getLogger("p2c")

class FileManager(object):
    def __init__(self):
        self.torrents = []

    def get_torrent_handler(self, torrent: Torrent, session):
        magnet = torrent.get_magnet()
        t_file = torrent.get_torrent_file()
        if t_file:
            source_type = "TORRENT"
            #raise Exception(t_file)
            parsed = urlparse(t_file, "http")
            url = parsed.geturl()
            target_path = os.path.join(settings.DOWNLOAD_DIR, parsed.path.split("/")[-1])
            source = urllib.request.urlretrieve(url, target_path)[0]
            #source = t_file
        else:
            source_type = "MAGNET"
            source = magnet

        for torrent_obj in self.torrents:
            if torrent_obj.source_type == source_type and\
               torrent_obj.source == source:
                return torrent_obj

        return self._create_torrent_handler(source_type, source, torrent.label, session)

    def prioritize_torrents(self, playing: Movie):
        for torrent in self.torrents:
            if playing.path in torrent.get_movies_filelist():
                # mark to download
                logger.info("downloading {}".format(torrent.name))
                torrent.download_file(playing.path)
            else:
                logger.debug("stopping {}".format(torrent.name))
                torrent.pause_download()

    def _create_torrent_handler(self, source_type, source, label, session):
        t_obj = TorrentObject(source_type, source, label)
        t_obj.bind_session(session)
        self.torrents.append(t_obj)
        return t_obj
