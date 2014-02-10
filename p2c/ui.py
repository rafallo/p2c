# -*- coding: utf-8 -*-
from p2c.info_clients.tmdbclient import TMDBApiClient

client = TMDBApiClient()

class TorrentInfo(object):
    def __init__(self, slug, label, seeders, leechers, kwargs):
        self.slug = slug
        self.label = label
        self.seeders = seeders
        self.leechers = leechers
        self.kwargs = kwargs

        self._info = None

    def get_magnet(self):
        return self.kwargs['magnet']

    def get_torrent_file(self):
        return self.kwargs['torrent_file']

    def get_availability_rate(self) -> int:
        """
        returns integer which values are described below:
        0 - no chance to download torrent
        1 - little change to smooth movie watching
        2 - probably you can watch it
        3 - perfect chance. A lot of seeds
        """
        if self.seeders == 0 and self.leechers == 0:
            return 0
        elif self.seeders < 50 and self.leechers < 200:
            return 1
        # twice more leechers than seeds or less than 1000 seeds
        elif self.seeders * 2 < self.leechers or self.seeders < 1000:
            return 2
        else:
            return 3

    def get_poster(self):
        if self._info is None:
            self._get_additional_info()
        if 'poster_path' in self._info and self._info['poster_path']:
            return client.base_url + self._info['poster_path']

    def get_verbose_title(self):
        if self._info is None:
            self._get_additional_info()
        return self._info.get('title', None)

    def get_description(self):
        if self._info is None:
            self._get_additional_info()
        desc = ""
        if 'release_date' in self._info:
            desc += "Release date: {}\n".format(self._info['release_date'])
        if 'vote_average' in self._info:
            desc += "Vote average: {}\n".format(self._info['vote_average'])
        return desc

    def _get_additional_info(self):
        self._info = {}
        self._info = client.match_title(self.label) or {}


class CategoryInfo(object):
    def __init__(self, slug: str, label:str, service,
                 kwargs:dict):
        self.slug = slug
        self.label = label
        self.service = service
        self.kwargs = kwargs

    def get_torrents(self, skip: int=0, limit: int=30) -> TorrentInfo:
        return self.service.get_torrents_list(self, skip=skip, limit=limit)
