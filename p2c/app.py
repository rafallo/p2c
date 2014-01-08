# -*- coding: utf-8 -*-
import json
import logging
import threading
from p2c import settings
from p2c.exceptions import SessionNotBindedException
from services.legittorrents import LegitTorrentsService
from services.tpb import TPBService
from torrent.manager import FileManager
from p2c.ui import Torrent
import libtorrent as lt
from torrent.movie import Movie

logger = logging.getLogger("p2c")

class Application(object):
    def __init__(self):
        self.manager = FileManager()
        self.services = [LegitTorrentsService(), TPBService()]
        self._init_session()

        threading.Thread(target=self._prefill_cache).start()

        self._playing = None

    def __del__(self):
        self._destroy_session()

    @property
    def session(self):
        if not self._session:
            raise SessionNotBindedException
        return self._session

    def buffer(self, movie:Movie):
        self.manager.prioritize_torrents(movie)

    def play(self, movie:Movie):
        self._playing = movie
        self.manager.prioritize_torrents(movie)

    def get_categories(self) -> list:
        output = []
        [output.extend(service.get_categories()) for service in self.services]
        return output

    def get_torrent(self, torrent: Torrent):
        return self.manager.get_torrent_handler(torrent, self.session)

    def _init_session(self):
        dht_state = self._get_storage_value("dht_state")
        if dht_state:
            ses = lt.session(dht_state)
        else:
            ses = lt.session()

        ses.listen_on(settings.START_PORT, settings.END_PORT)
        self._session = ses

    def _destroy_session(self):
        ses = self.session
        state = None
        try:
            state = ses.dht_state()
        except:
            logger.warning("""
                UnicodeEncodeError raised by dht_state\nsee
                http://code.google.com/p/libtorrent/issues/detail?id=449
                for more details
                """)
        if state:
            self._save_storage_value("dht_state", state)

    def _get_storage_value(self, key):
        data = self._get_storage_data()
        return data.get(key, None
        )

    def _save_storage_value(self, key, value):
        data = self._get_storage_data()
        data[key] = value

        f = open(settings.STORAGE_PATH, "w")
        json.dump(data, f)
        f.close()

    def _get_storage_data(self):
        f = None
        try:
            f = open(settings.STORAGE_PATH, "r")
        except IOError:
            logger.info("storage file does not exists.")
        data = {}

        if f:
            try:
                data = json.load(f)
            except TypeError:
                logger.error("storage file is corrupted. Overwriting.")

        if isinstance(data, dict):
            logger.error("storage data is not a dict. Overwriting.")
            data = {}
        return data

    def _prefill_cache(self):
        for category in self.get_categories()[:20]:
            category.get_torrents()




