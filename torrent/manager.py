# -*- coding: utf-8 -*-
import base64
import hashlib
from threading import Thread
import os
import logging
from urllib.parse import urlparse
import urllib.request
from p2c import settings
from torrent.torrent import Torrent
from torrent.movie import Movie

logger = logging.getLogger(__name__)

class FileManager(object):
    def __init__(self):
        self.torrents = {}

        #torrent: TorrentInfo
    def get_torrent_handler(self, label, session, magnet=None, t_file=None):
        assert(magnet or t_file)
        source_path = None
        url = None
        if t_file:
            source_type = "TORRENT"
            parsed = urlparse(t_file, "http")
            url = parsed.geturl()
            source_path = os.path.join(settings.DOWNLOAD_DIR,
                (base64.b64encode(url.encode()).decode() + ".torrent"))
        else:
            source_type = "MAGNET"
            source = magnet

        for id in self.torrents:
            torrent_obj = self.torrents[id]
            if torrent_obj.source_type == "TORRENT":
                if id == self._get_torrent_uniqueness(source_path):
                    return torrent_obj
                else:
                    pass
            else:
                if torrent_obj.source_type == source_type and\
                   id == self._get_torrent_uniqueness(source):
                    return torrent_obj

        if source_type == "TORRENT":
            def retrieve_and_save(url, source_path, session, t_obj):
                source = urllib.request.urlretrieve(url, source_path)[0]
                t_obj.set_source(source, session)

            t_obj = self._create_torrent_handler(source_type, None,
                source_path, label, session)
            Thread(target=retrieve_and_save,
                args=(url, source_path, session, t_obj)).start()
            return t_obj
        else:
            return self._create_torrent_handler(source_type, source,
                source_path, label, session)

    def prioritize_torrents(self, playing: Movie):
        for torrent in self.torrents.values():
            if playing.path in torrent.get_movies_filelist():
                # mark to download
                logger.info("downloading {}".format(torrent.name))
                torrent.download_file(playing.path)
            else:
                logger.debug("stopping {}".format(torrent.name))
                torrent.pause_download()

    def _create_torrent_handler(self, source_type, source, source_path, label,
                                session):
        id = self._get_torrent_uniqueness(
            source_path if source_type == "TORRENT" else source)
        t_obj = Torrent(source_type, source, label)
        # TODO: make it asynchronous
        t_obj.set_source(source, session)
        self.torrents[id]=t_obj
        return t_obj

    def _get_torrent_uniqueness(self, data):
        return hashlib.md5(data.encode("utf-8")).digest()
