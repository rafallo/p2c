# -*- coding: utf-8 -*-
import gzip
from io import StringIO
from urllib import request
from bs4 import BeautifulSoup
from catalogs.services.base import  BaseService
from p2c.ui import CategoryInfo

_ = lambda x: x


class KickAssService(BaseService):
    name = "Kick Ass"
    category_url = "http://kickass.to/{category_id}/{page}/?field=seeders&sorder=desc"
    search_url = "http://kickass.to/usearch/{phrase}%20category:movies/{page}/"
    page_size = 25
    video_category_id = "movies"

    domain = "http://kickass.to/"

    def get_categories(self) -> list:
        return [
            CategoryInfo(id='movies',
                label=_("Movies"),
                service=self),
            CategoryInfo(id='3d-movies',
                label=_("3D movies"),
                service=self)]

    def _get_html_containers(self, category_id, page, query):
        # for BS parsing. Returns html container with torrent data
        if query:
            if category_id:
                url = self.search_url.format(
                    category_id=category_id,
                    page=page,
                    phrase=query
                )
            else:
                url = self.search_url.format(
                    category_id=self.video_category_id,
                    page=page,
                    phrase=query
                )
        else:
            url = self.category_url.format(
                category_id=category_id,
                page=page
            )
        site = request.urlopen(url)
        content = site.read()
        if site.info().get('Content-Encoding') == 'gzip':
            content = gzip.decompress(content)
        soup = BeautifulSoup(content)
        for container in soup.find("div", "mainpart").find("table", "doublecelltable").find("table").find_all("tr", {'class': ('odd', 'even')}):
            if self._is_valid_html_container(container):
                yield container

    def _is_valid_html_container(self, container):
        return True

    def _parse_html_container(self, container):
        name = container.find("div", "torrentname").find("a", "plain").text
        torrent_file = container.find_all("a", "idownload")[1].get('href')
        # TODO: due https://github.com/rafallo/p2c/issues/1 disabled temporarily.
        torrent_file = None
        magnet = container.find("a", "imagnet").get('href')
        seeders = container.find("td", "green center").text
        leechers = container.find("td", "red lasttd center").text
        return (name, torrent_file, magnet, seeders, leechers)

