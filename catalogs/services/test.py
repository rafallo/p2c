# -*- coding: utf-8 -*-
from unittest import TestCase
from catalogs.services.base import BaseService
from catalogs.services.tpb import TPBService
from p2c.ui import TorrentInfo, CategoryInfo

class TPBServiceTestCase(TestCase):
    def setUp(self):
        self.service = TPBService()

    def test_get_categories(self):
        categories = self.service.get_categories()
        self.assertIsInstance(categories, list)

    def test_get_torrents(self):
        first_category = self.service.get_categories()[0]
        torrents = self.service.get_torrents_list(first_category)
        self.assertIsInstance(torrents, list)
        for torrent in torrents:
            self.assertIsInstance(torrent, TorrentInfo)


class TestBaseService(BaseService):
    video_category_id = 1
    page_size = 8
    def get_categories(self):
        return [
            CategoryInfo(slug='movies',
                label="Movies",
                service=self,
                kwargs={'id': 1})]

    def _get_html_containers(self, category_id, page, query):
        for i in range(0, self.page_size):
            yield ("Movie %s" % i, "http://127.0.0.1:8567/movie.torrent", None, 1000, 2000)

    def _is_valid_html_container(self, container):
        return True

    def _parse_html_container(self, container):
        return container

class BaseServiceTestCase(TestCase):
    def setUp(self):
        self.service = TestBaseService()

    def test_get_categories(self) -> CategoryInfo:
#        server = HTTPServer(('0.0.0.0', 8567), TestSimpleHTTPRequestHandler)
#        th = Thread(target=server.serve_forever)
#        th.daemon = True
#        th.start()
        categories = self.service.get_categories()
        self.assertIsInstance(categories, list)
        self.assertIsInstance(categories[0], CategoryInfo)
        return categories[0]

    def test_get_torrents(self):
        category = self.test_get_categories()
        torrents = category.get_torrents(0, 10)
        self.assertIsInstance(torrents, list)
        self.assertEqual(len(torrents), 10)
        for torrent in torrents:
            self.assertIsInstance(torrent, TorrentInfo)

