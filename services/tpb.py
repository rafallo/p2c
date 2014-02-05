# -*- coding: utf-8 -*-
from urllib import request
from bs4 import BeautifulSoup
import re
from.base import BaseService
from p2c.ui import Category

_ = lambda x: x


class TPBService(BaseService):
    name = "The Pirate Bay"
    category_url = "http://thepiratebay.se/browse/{category_id}/{page}/7"
    search_url = "http://thepiratebay.se/search/{phrase}/{page}/7/" + str(200)
    page_size = 30
    video_category_id = 200

    def get_categories(self) -> list:
        return [
            Category(slug='movies',
                label=_("Movies"),
                service=self,
                kwargs={'id': 201}),
            Category(slug='movies_dvdr',
                label=_("Movies DVDR"),
                service=self,
                kwargs={'id': 202}),
            Category(slug='music_videos',
                label=_("Music videos"),
                service=self,
                kwargs={'id': 203}),
            Category(slug='movie_clips',
                label=_("Movie clips"),
                service=self,
                kwargs={'id': 204}),
            Category(slug='tv_shows',
                label=_("TV shows"),
                service=self,
                kwargs={'id': 205}),
            Category(slug='handheld',
                label=_("Handheld"),
                service=self,
                kwargs={'id': 206}),
            Category(slug='hd_movies',
                label=_("HD - Movies"),
                service=self,
                kwargs={'id': 207}),
            Category(slug='hd_tv_shows',
                label=_("HD - TV shows"),
                service=self,
                kwargs={'id': 208}),
            Category(slug='3d',
                label=_("3D"),
                service=self,
                kwargs={'id': 209}),
            Category(slug='other',
                label=_("Other"),
                service=self,
                kwargs={'id': 299}),
            ]

    def _get_html_containers(self, category_id, page):
        # for BS parsing. Returns html container with torrent data
        site = request.urlopen(self.category_url.format(
            category_id=category_id,
            page=page
        ))
        soup = BeautifulSoup(site.read())
        for container in soup.find(id="searchResult").children:
            if self._is_valid_html_container(container):
                yield container

    def _is_valid_html_container(self, container):
        # for BS parsing. Checks if html containr is valid
        try:
            if not container.name == "tr":
                return False
        except:
            return False
        name_el = container.find('a', {'class': 'detLink'})
        if not name_el:
            return False
        return True

    def _parse_html_container(self, container):
        # for BS parsing. Parses html container and returns proper data
        name = container.find('a', {'class': 'detLink'}).text

        torrent_file = None
        magnet = None

        magnet_el = container.find('a', {'href': re.compile("^magnet")})
        if magnet_el:
            magnet = magnet_el.get('href')

        file_el = container.find('a', {'href': re.compile("\.torrent$")})
        if file_el:
            torrent_file = file_el.get('href')

        seeders, leechers = [int(item.text) for item in
                             container.find_all('td')[2:4]]
        return (name, torrent_file, magnet, seeders, leechers)

