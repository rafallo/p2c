# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from p2c.ui import Category

class AbstractService(metaclass=ABCMeta):
    @abstractmethod
    def get_categories(self) -> list:
        pass

    @abstractmethod
    def get_torrents_list(self, category : Category=None, skip: int=0,
                          limit: int=30) -> list:
        pass


