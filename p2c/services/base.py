# -*- coding: utf-8 -*-
from abc import abstractmethod
from threading import Thread, Lock
from .abstractbase import AbstractService
from p2c.ui import CategoryInfo, TorrentInfo
from p2c.utils import slugify

_ = lambda x: x


class BaseService(AbstractService):
    name = None
    category_url = None
    search_url = None
    page_size = None
    video_category_id = None
    
    torrents = dict()
    torrents_mutex = Lock()
    running_threads = dict()

    def __init__(self):
        pass

    @abstractmethod
    def get_categories(self) -> list:
        pass
    
    def get_torrents_list(self, category : CategoryInfo=None, skip: int=0,
                          limit=None) -> list:
        if limit is None:
            limit = self.page_size
        # category.id or base video category
        category_id = category.kwargs[
                      'id'] if category else self.video_category_id

        # count current TPB pa  ge and quantity of page to retrieve
        page = int(skip / self.page_size)
        page_count = ((skip % self.page_size) + limit - 1) / (self.page_size + 1)
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
        start = page * self.page_size
        limit = start + self.page_size
        retrieved = category_id in self.torrents\
                    and len(self.torrents[category_id]) > limit\
        and not None in self.torrents[category_id][start:limit]

        key = (category_id, page)
        if force or (not retrieved):
            if not key in self.running_threads:
                thread = Thread(target=self._thread_retrieve_torrents,
                    args=(category_id, page))
                thread.start()
                self.running_threads[key] = thread

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
            torrent = TorrentInfo(slug=slugify(name),
                label=name,
                seeders=seeders,
                leechers=leechers,
                kwargs=kwargs
            )
            self.torrents_mutex.acquire()
            # filling self.torrents[category_id] with values or None values
            # for proper list length
            place = page * self.page_size + counter
            if len(self.torrents[category_id]) <= place:
                list_fill_len = page * self.page_size - len(
                    self.torrents[category_id]) + self.page_size
                self.torrents[category_id].extend(
                    [None for i in range(0, list_fill_len)])
                self.torrents[category_id][
                page * self.page_size + counter] = torrent
            self.torrents[category_id][
            page * self.page_size + counter] = torrent

            self.torrents_mutex.release()

    @abstractmethod
    def _get_html_containers(self, category_id, page):
        pass

    @abstractmethod
    def _is_valid_html_container(self, container):
        pass

    @abstractmethod
    def _parse_html_container(self, container):
        pass

