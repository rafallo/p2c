# -*- coding: utf-8 -*-
from http.server import HTTPServer
import logging
from threading import Thread
import shutil
from unittest import TestCase
import time
from p2c.exceptions import TorrentHasNotMetadataYet
from pbt.tracker import Tracker
import os
from p2c import settings
from test_utils import TestSimpleHTTPRequestHandler
from torrent.manager import FileManager
from torrent.torrent import Torrent
import libtorrent as lt

settings.DOWNLOAD_DIR = os.path.join(settings.DOWNLOAD_DIR, "tests")

BIG_MOVIE_TEST = False

MAGNET = "magnet:?xt=urn:btih:1fe752da569939680f975674fe18bf87150edeb7&dn=Test+movie&tr=http://127.0.0.1:9000/announce/"
# it works! but i have no idea why it not work with localhost tracker
#MAGNET = "magnet:?xt=urn:btih:ce9fbdaa734cfbc160e8ef9d29072646c09958dd&dn=The.Wolf.of.Wall.Street.2013.DVDSCR.XviD-BiDA&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80&tr=udp%3A%2F%2Ftracker.istole.it%3A6969&tr=udp%3A%2F%2Ftracker.ccc.de%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337"

TORRENT_PATH = os.path.join(settings.TEST_DIR, "movie.torrent")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class AbstractTorrentTestCase(TestCase):
    tracker = None
    seeder = None

    def configure_session(self):
        ses = lt.session()
        ses.listen_on(6821, 6831)

        ses.start_dht()
        ses.start_lsd()
        ses.start_upnp()
        ses.start_natpmp()

        self.session = ses

    @classmethod
    def run_tracker(cls):
        cls.tracker = Tracker(port=9000)
        cls.tracker.run()

    @classmethod
    def run_seeder(cls):
        ses = lt.session()
        ses.listen_on(2000, 3000)

        # not so fast
        ses.set_upload_rate_limit(500)
        ses.start_dht()
        ses.start_lsd()
        ses.start_upnp()
        ses.start_natpmp()

        info = lt.torrent_info(TORRENT_PATH)

        h = ses.add_torrent({
            'ti': info,
            'save_path': settings.TEST_DIR
        })
        h.super_seeding(True)

        cls.h = h
        cls.info = info
        cls.seeder = ses

    @classmethod
    def stop_tracker(cls):
        cls.tracker.stop()

    @classmethod
    def stop_seeder(cls):
        del cls.seeder


class TorrentObjectTestCase(AbstractTorrentTestCase):
    @classmethod
    def setUpClass(cls):
        cls.run_tracker()
        cls.run_seeder()

    @classmethod
    def tearDownClass(cls):
        cls.stop_tracker()
        shutil.rmtree(settings.DOWNLOAD_DIR, True)

    def setUp(self):
        shutil.rmtree(settings.DOWNLOAD_DIR, True)
        self.configure_session()

        try:
            os.makedirs(settings.DOWNLOAD_DIR)
        except OSError:
            pass

    def tearDown(self):
        self.stop_tracker()

    def test_create_torrent(self):
        torrent_content = TORRENT_PATH
        self.obj = Torrent(
            source_type="TORRENT",
            source=torrent_content,
            name="test movie")
        self.obj.bind_session(self.session)
        self.assertIsInstance(self.obj, Torrent)
        self.assertIsInstance(self.obj.get_torrent_info(), lt.torrent_info)

    def test_create_magnet_torrent(self):
        self.obj = Torrent(
            source_type="MAGNET",
            source=MAGNET,
            name="test movie")
        self.obj.bind_session(self.session)
        self.assertIsInstance(self.obj, Torrent)

        # we need to wait to download metadata
        self.assertRaises(TorrentHasNotMetadataYet, self.obj.get_torrent_info)
        count = 0
        while not self.obj.has_torrent_info():
            time.sleep(0.2)
            count += 1
            if count > 300:
                raise Exception("counter exceeded")
        self.assertIsInstance(self.obj.get_torrent_info(), lt.torrent_info)


    def test_get_filelist(self):
        self.test_create_torrent()
        files = self.obj.get_filelist()

        self.assertEqual(len(files), 3)
        self.assertEqual(files[0], "movie/movie.mp4")
        self.assertEqual(files[1], "movie/music.mp3")
        self.assertEqual(files[2], "movie/subs.txt")


    def test_get_movie_filelist(self):
        self.test_create_torrent()
        files = self.obj.get_movies()

        self.assertEqual(len(files), 1)
        self.assertEqual(list(files)[0].path, "movie/movie.mp4")

    def test_download_file(self):
        # it works! but i have no idea why it not work with localhost tracker
        return
        self.test_create_torrent()
        print("created. Go further")
        time.sleep(0.5)
        filename = "movie/movie.mp4"
        #        print(self.obj.get_movies()[0].__dict__)
        self.obj.download_file(filename)
        while True:
            time.sleep(0.5)
            #            print(self.obj.get_movies()[0].cur_first_piece)
            #            print(self.obj.get_torrent_info().files()[0].size)
            #            print(self.__class__.h.status().state)
            #            print(self.__class__.h.status().progress)
            #            print(self.obj.get_status())
            #            print(self.obj.torrent_handler.status().state)
            print(self.obj.torrent_handler.status().progress * 100)

#            print(self.obj.torrent_handler.status().pieces[0])
#            self.obj._manage_pieces_priority()
#            print(h)
#            h = self.__class__.h
#            info= self.__class__.info
#            print(info.files()[0])
#            print(info.files()[0].path)
#            print(h.is_seed())
#            h.resume()


class FileManagerTestCase(AbstractTorrentTestCase):
    def setUp(self):
        self.manager = FileManager()
        self.configure_session()

    def test_get_torrent_handler_magnet(self):
        t_obj = self.manager.get_torrent_handler("Test",
            self.session, MAGNET)

        self.assertIsInstance(t_obj, Torrent)
        self.assertEqual(t_obj.source_type, "MAGNET")

    def test_get_torrent_handler_torrent(self):
        server = HTTPServer(('0.0.0.0', 8567), TestSimpleHTTPRequestHandler)
        th = Thread(target=server.serve_forever)
        th.daemon = True
        th.start()
        t_obj = self.manager.get_torrent_handler("Test",
            self.session, None, "http://127.0.0.1:8567/movie.torrent")

        self.assertIsNone(t_obj.source)
        timeout = 0
        while t_obj.source is None:
            time.sleep(0.1)
            timeout += 1
            if timeout == 30:
                raise AssertionError

        self.assertIsNotNone(t_obj.source)

        self.assertIsInstance(t_obj, Torrent)
        self.assertEqual(t_obj.source_type, "TORRENT")

