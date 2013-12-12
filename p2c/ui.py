# -*- coding: utf-8 -*-
class Category(object):
    def __init__(self, slug: str, label:str, service,
                 kwargs:dict):
        self.slug = slug
        self.label = label
        self.service = service
        self.kwargs = kwargs

    def get_torrents(self, skip: int=0, limit: int=30):
        return self.service.get_torrents_list(self, skip=skip, limit=limit)


class Torrent(object):
    def __init__(self, slug, label, seeders, leechers, kwargs):
        self.slug = slug
        self.label = label
        self.seeders = seeders
        self.leechers = leechers
        self.kwargs = kwargs

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