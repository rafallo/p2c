# -*- coding: utf-8 -*-
import shutil
from unittest import TestCase
import time
from p2c.exceptions import TorrentHasNotMetadataYet
from pbt.tracker import Tracker
import os
from p2c import settings
from p2c.torrent.torrent import TorrentObject
import libtorrent as lt

settings.DOWNLOAD_DIR = os.path.join(settings.DOWNLOAD_DIR, "tests")

BIG_MOVIE_TEST = False

MAGNET = "magnet:?xt=urn:btih:ceb7dce3a94ac172bc6c5f7ca056d99a47029f0f&dn=Test+movie&tr=http://127.0.0.1:9000/"
TORRENT_PATH = os.path.join(settings.TEST_DIR, "movie.torrent")
if BIG_MOVIE_TEST:
    MAGNET = "magnet:?xt=urn:btih:cc98fcb95f35d77de86ddc4cc76ca30f338eb322&dn=Big+movie&tr=http://127.0.0.1:9000/"
    TORRENT_PATH = os.path.join(settings.TEST_DIR, "big_movie.torrent")

    #MAGNET = "magnet:?xt=urn:btih:7238a0a1343e4feb43a4f3f0fefe062bbd220dcc&dn=House.Of.Cards.2013.S01.WEBRip.x264-TRiC&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80&tr=udp%3A%2F%2Ftracker.istole.it%3A6969&tr=udp%3A%2F%2Ftracker.ccc.de%3A80"

class TorrentObjectTestCase(TestCase):
    tracker = None
    seeder = None

    @classmethod
    def setUpClass(cls):

        cls.run_tracker()
        cls.run_seeder()

    @classmethod
    def tearDownClass(cls):
        cls.stop_tracker()
        shutil.rmtree(settings.DOWNLOAD_DIR, True)

    def setUp(self):
        self.configure_session()
        shutil.rmtree(settings.DOWNLOAD_DIR, True)

        try:
            os.makedirs(settings.DOWNLOAD_DIR)
        except OSError:
            pass

    def tearDown(self):
        self.stop_tracker()

    def test_create_torrent(self):
        torrent_content = TORRENT_PATH
        self.obj = TorrentObject(
            source_type="TORRENT",
            source=torrent_content,
            name="test movie")
        self.obj.bind_session(self.session)
        self.assertIsInstance(self.obj, TorrentObject)
        self.assertIsInstance(self.obj.get_torrent_info(), lt.torrent_info)

    def test_create_magnet_torrent(self):

        self.obj = TorrentObject(
            source_type="MAGNET",
            source=MAGNET,
            name="test movie")
        self.obj.bind_session(self.session)
        self.assertIsInstance(self.obj, TorrentObject)

#        we need to wait to download metadata
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
        self.assertEqual(files[0], "movie/music.mp3")
        self.assertEqual(files[1], "movie/sintel.mp4")
        self.assertEqual(files[2], "movie/sintel.txt")


    def test_get_movie_filelist(self):
        self.test_create_torrent()
        files = self.obj.get_movies()

        self.assertEqual(len(files), 1)
        self.assertEqual(list(files)[0].path, "movie/sintel.mp4")

    def test_download_file(self):
        return
        self.test_create_torrent()
        filename = "movie/sintel.mp4"
        if BIG_MOVIE_TEST:
            filename = "big_movie/trust.avi"
            #filename = "House.Of.Cards.2013.S01.WEBRip.x264-TRiC/House.Of.Cards.2013.S01E09.WEBRip.x264-TRiC.mp4"
        self.obj.download_file(filename)
        while True:
            time.sleep(0.5)
            print(self.obj.torrent_handler.file_progress())
            self.obj._manage_pieces_priority()


    def configure_session(self):
        ses = lt.session()
        ses.listen_on(6821, 6831)

#        set = lt.dht_settings()
#        set.restrict_routing_ips = False
#        set.restrict_search_ips = False
#        ses.set_dht_settings(set)
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

#        set = lt.dht_settings()
#        set.restrict_routing_ips = False
#        set.restrict_search_ips = False
#        ses.set_dht_settings(set)
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
        cls.seeder = ses

    @classmethod
    def stop_tracker(cls):
        cls.tracker.stop()

    @classmethod
    def stop_seeder(cls):
        del cls.seeder
