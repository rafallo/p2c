# -*- coding: utf-8 -*-
from catalogs.info_clients.tmdbclient import TMDBApiClient

client = TMDBApiClient()

class TorrentInfo(object):
    def __init__(self, slug, label, seeders, leechers, kwargs):
        self.slug = slug
        self.label = label
        self.seeders = seeders
        self.leechers = leechers
        self.kwargs = kwargs

        self.description = None
        self.poster = None
        self.title = None

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
        # twice more leechers tinfohan seeds or less than 1000 seeds
        elif self.seeders * 2 < self.leechers or self.seeders < 1000:
            return 2
        else:
            return 3

    def get_additional_info(self):
        info = client.match_title(self.label) or {}

        self.title = info.get('title', None)
        if 'poster_path' in info and info['poster_path']:
            self.poster = client.base_url + info['poster_path']

        if 'release_date' in info or 'vote_average' in info:
            self.description = ""
            if 'release_date' in info:
                self.description += "Release date: {}\n".format(info['release_date'])
            if 'vote_average' in info:
                self.description += "Vote average: {}\n".format(info['vote_average'])



class CategoryInfo(object):
    def __init__(self, slug: str, label:str, service,
                 kwargs:dict):
        self.slug = slug
        self.label = label
        self.service = service
        self.kwargs = kwargs

    def get_torrents(self, skip: int=0, limit: int=30) -> TorrentInfo:
        return self.service.get_torrents_list(self, skip=skip, limit=limit)
