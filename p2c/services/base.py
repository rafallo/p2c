# -*- coding: utf-8 -*-
from threading import Thread, Lock
from.abstractbase import AbstractService
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

    def get_categories(self) -> list:
        raise NotImplementedError

    def _get_torrents(self, category_id, skip, limit, query):
        # count current TPB pa  ge and quantity of page to retrieve
        page = int(skip / self.page_size)
        page_count = ((skip % self.page_size) + limit) / (self.page_size)
        if page_count % 1 != 0:
            page_count = int(page_count) + 1
        else:
            page_count = int(page_count)
        page_range = page + page_count
        for i in range(page, page_range):
            self._retrieve_torrents(category_id, i, query)

        # retrieve limit +1 for smooth using
        for i in range(page_range, page_range + page_count):
            self._retrieve_torrents(category_id, i, query, wait=False)

    def search(self, query: str, skip: int=0, limit=None) -> list:
        if limit is None:
            limit = self.page_size
        self._get_torrents(None, skip, limit, query)
        return [i for i in self.torrents[(None, query)][skip:limit + skip]  if
                i is not None]

    def get_torrents_list(self, category : CategoryInfo=None, skip: int=0,
                          limit=None) -> list:
        if limit is None:
            limit = self.page_size
            # category.id or base video category
        category_id = category.kwargs[
                      'id'] if category else self.video_category_id

        self._get_torrents(category_id, skip, limit, None)
        return [i for i in self.torrents[(category_id, None)][skip:limit + skip]
                if i is not None]

    def _retrieve_torrents(self, category_id : int, page:int, query: str,
                           wait:bool=True,
                           force:bool=False):
        start = page * self.page_size
        limit = start + self.page_size
        key = (category_id, query)
        retrieved = category_id in self.torrents\
                    and len(self.torrents[key]) > limit\
        and not None in self.torrents[key][start:limit]

        th_key = (category_id, page, query)
        if force or (not retrieved):
            if not th_key in self.running_threads:
                thread = Thread(target=self._thread_retrieve_torrents,
                    args=(category_id, page, query))
                thread.start()
                self.running_threads[th_key] = thread

        if wait and th_key in self.running_threads:
            self.running_threads.pop(th_key).join()

    def _thread_retrieve_torrents(self, category_id : int, page: int,
                                  query: str):
        # retrieves torrent parsing tpb site

        key = (category_id, query)

        if not key in self.torrents:
            self.torrents_mutex.acquire()
            self.torrents[key] = list()
            self.torrents_mutex.release()

        for counter, container in enumerate(
            self._get_html_containers(category_id, page, query)):
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
            # filling self.torrents[key] with values or None values
            # for proper list length
            place = page * self.page_size + counter
            if len(self.torrents[key]) <= place:
                list_fill_len = page * self.page_size - len(
                    self.torrents[key]) + self.page_size
                self.torrents[key].extend(
                    [None for i in range(0, list_fill_len)])
                self.torrents[key][
                page * self.page_size + counter] = torrent
            self.torrents[key][
            page * self.page_size + counter] = torrent

            self.torrents_mutex.release()

    def _get_html_containers(self, category_id, page, query):
        """
        get html container from page
        """
        raise NotImplementedError

    def _is_valid_html_container(self, container):
        raise NotImplementedError

    def _parse_html_container(self, container):
        raise NotImplementedError

