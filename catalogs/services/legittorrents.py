# -*- coding: utf-8 -*-
from urllib import request
from bs4 import BeautifulSoup
from catalogs.services.base import  BaseService
from p2c.ui import CategoryInfo

_ = lambda x: x


class LegitTorrentsService(BaseService):
    name = "Legit Torrents"
    category_url = "http://www.legittorrents.info/index.php?page=torrents&order=5&by=2&category={category_id}&active=1&pages={page}"
    search_url = "http://www.legittorrents.info/index.php?page=torrents&order=5&by=2&category={category_id}&active=1&pages={page}&search={phrase}"
    page_size = 18
    video_category_id = 1

    domain = "http://www.legittorrents.info/"

    def get_categories(self) -> list:
        return [
            CategoryInfo(slug='movies',
                label=_("Movies"),
                service=self,
                kwargs={'id': 1})]

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
        soup = BeautifulSoup(site.read())

        for container in soup.find_all("table", "lista")[3].find_all("tr")[1:]:
            if self._is_valid_html_container(container):
                yield container

    def _is_valid_html_container(self, container):
        # for BS parsing. Checks if html containr is valid
        if len(list(container.children)) < 4:
            return False
        return True

    def _parse_html_container(self, container):
        # for BS parsing. Parses html container and returns proper data
        name = container.find_all('td')[1].find('a').text

        torrent_file = None
        magnet = None
        torrent_file = self.domain + container.find_all('td')[2].find('a').get('href')
        seeders, leechers = [int(item.text) for item in
                             container.find_all('td')[4:6]]
        return (name, torrent_file, magnet, seeders, leechers)

