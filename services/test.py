# -*- coding: utf-8 -*-
from unittest import TestCase
from p2c.services.tpb import TPBService
from p2c.ui import Torrent

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
            self.assertIsInstance(torrent, Torrent)
