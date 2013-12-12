# -*- coding: utf-8 -*-
from threading import Thread, Lock
from collections import defaultdict
from urllib import request
from bs4 import BeautifulSoup
import re
import time
from.base import AbstractService
from p2c.ui import Category, Torrent
from p2c.utils import slugify

_ = lambda x: x

# order by seeders
TPB_VIDEO_CATEGORY_ID = 200
TPB_CATEGORY_URL = "http://thepiratebay.se/browse/{category_id}/{page}/7"
TPB_SEARCH_URL = "http://thepiratebay.se/search/{phrase}/{page}/7/" + str(TPB_VIDEO_CATEGORY_ID)
TPB_PAGE_SIZE = 30

class TPBService(AbstractService):
    torrents = dict()

    torrents_mutex = Lock()
    running_threads = dict()

    def __init__(self):
        pass

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

    def get_torrents_list(self, category : Category=None, skip: int=0,
                          limit: int=TPB_PAGE_SIZE) -> list:
        # category.id or base video category
        category_id = category.kwargs[
                      'id'] if category else TPB_VIDEO_CATEGORY_ID

        # count current TPB pa  ge and quantity of page to retrieve
        page = int(skip / TPB_PAGE_SIZE)
        page_count = ((skip % TPB_PAGE_SIZE) + limit - 1) / (TPB_PAGE_SIZE + 1)
        if page_count % 1 != 0:
            page_count = int(page_count) + 1
        else:
            page_count = int(page_count)
        page_range = page + page_count
        for i in range(page, page_range):
            self._retrieve_torrents(category_id, i)

        # retrieve limit +1 for smooth using
        for i in range(page_range, page_range + page_count):
            self._retrieve_torrents(category_id, i, wait=False)

        return self.torrents[category_id][skip:limit + skip]

    def _retrieve_torrents(self, category_id : int, page:int, wait:bool=True,
                           force:bool=False):
        start = page * TPB_PAGE_SIZE
        limit = start + TPB_PAGE_SIZE
        retrieved = category_id in self.torrents\
                    and len(self.torrents[category_id]) > limit\
        and not None in self.torrents[category_id][start:limit]

        key = (category_id, page)
        if force or (not retrieved):
            if not key in self.running_threads:
                thread = Thread(target=self._thread_retrieve_torrents,
                    args=(category_id, page))
                self.running_threads[key] = thread
                thread.start()

        if wait and key in self.running_threads:
            self.running_threads.pop(key).join()

    def _thread_retrieve_torrents(self, category_id : int, page: int):
        # retrieves torrent parsing tpb site
        if not category_id in self.torrents:
            self.torrents[category_id] = list()

        for counter, container in enumerate(
            self._get_html_containers(category_id, page)):
            name,\
            torrent_file,\
            magnet,\
            seeders,\
            leechers = self._parse_html_container(container)

            kwargs = {'magnet': magnet,
                      'torrent_file': torrent_file
            }
            torrent = Torrent(slug=slugify(name),
                label=name,
                seeders=seeders,
                leechers=leechers,
                kwargs=kwargs
            )
            self.torrents_mutex.acquire()
            # filling self.torrents[category_id] with values or None values
            # for proper list length
            place = page * TPB_PAGE_SIZE + counter
            if len(self.torrents[category_id]) <= place:
                list_fill_len = page * TPB_PAGE_SIZE - len(
                    self.torrents[category_id]) + TPB_PAGE_SIZE
                self.torrents[category_id].extend(
                    [None for i in range(0, list_fill_len)])
                self.torrents[category_id][
                page * TPB_PAGE_SIZE + counter] = torrent
            self.torrents[category_id][
            page * TPB_PAGE_SIZE + counter] = torrent

            self.torrents_mutex.release()

    def _get_html_containers(self, category_id, page):
        # for BS parsing. Returns html container with torrent data
        site = request.urlopen(TPB_CATEGORY_URL.format(
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

