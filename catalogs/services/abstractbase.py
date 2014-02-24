# -*- coding: utf-8 -*-
from p2c.ui import CategoryInfo

class AbstractService(object):

    def get_categories(self) -> list:
        raise NotImplementedError

    def get_torrents_list(self, category : CategoryInfo=None, skip: int=0,
                          limit: int=30) -> list:
        raise NotImplementedError


