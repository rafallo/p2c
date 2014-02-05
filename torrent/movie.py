# -*- coding: utf-8 -*-
import os
import logging
from p2c import settings
from p2c.exceptions import NotDownloadingException

logger = logging.getLogger("p2c")

class Movie(object):
    def __init__(self, path, size, first_piece, last_piece, piece_length, download_dir):
        self.path = path
        self.size = size
        self.first_piece = first_piece
        self.last_piece = last_piece
        self.cur_first_piece = first_piece
        self.cur_last_piece = last_piece
        self.piece_length = piece_length
        self.download_dir = download_dir
        self.downloaded_pieces = 0

    def __str__(self):
        return self.path

    @property
    def name(self):
        return os.path.split(self.path)[-1]

    @property
    def progress(self):
        return float(self.downloaded_pieces) / \
               float(self.last_piece - self.first_piece)

    def can_play(self):
        # TODO: make it better, more intelligent
        # if downloaded block is greater than DOWNLOAD_PIECE_SIZE
        logger.debug("downloaded pieces: {}, piece_length: {}".format(self.downloaded_pieces, self.piece_length))
        if self.downloaded_pieces * self.piece_length > settings.DOWNLOAD_PIECE_SIZE:
            return True
        return False

    def get_target_path(self):
        return os.path.join(self.download_dir, self.path)
