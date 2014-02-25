# -*- coding: utf-8 -*-
import logging
from urllib import request
from bs4 import BeautifulSoup
import re
from catalogs.services.base import BaseService
from p2c.ui import CategoryInfo

_ = lambda x: x

logger = logging.getLogger(__name__)


class TPBService(BaseService):
    name = "The Pirate Bay"
    category_url = "http://thepiratebay.se/browse/{category_id}/{page}/7"
    search_url = "http://thepiratebay.se/search/{phrase}/{page}/7/{category_id}"
    page_size = 30
    video_category_id = 200

    def get_categories(self) -> list:
        return [
            CategoryInfo(id='201',
                label=_("Movies"),
                service=self),
            CategoryInfo(id='202',
                label=_("Movies DVDR"),
                service=self),
            CategoryInfo(id='205',
                label=_("TV shows"),
                service=self),
            CategoryInfo(id='207',
                label=_("HD - Movies"),
                service=self),
            CategoryInfo(id='208',
                label=_("HD - TV shows"),
                service=self),
            CategoryInfo(id='209',
                label=_("3D"),
                service=self),
            ]

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
                    category_id=200,
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
        if(soup.find(id="searchResult")):
            for container in soup.find(id="searchResult").children:
                if self._is_valid_html_container(container):
                    yield container
        else:
            logger.debug("No #searchResult in html file")

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

