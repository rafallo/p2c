# -*- coding: utf-8 -*-
import hashlib
import libtorrent as lt
import logging
from threading import Timer, Thread, Condition, Event
import os
import time
from p2c import settings
from p2c.exceptions import SessionNotBindedException, TorrentHasNotMetadataYet
from torrent.movie import Movie

SOURCE_TYPES = ("MAGNET", "TORRENT")

logger = logging.getLogger("p2c")

class TorrentObject(object):
    def __init__(self, source_type, source, name):
        """
        :type source: str magnet or torrent file path
        :type name: str
        :type source_type: str

        """
        if not source_type in SOURCE_TYPES:
            raise Exception(
                "source_type must be one of {0}".format(SOURCE_TYPES))

        self.name = name
        self.source_type = source_type
        self.source = source

        self.torrent_handler = None
        self._torrent_info = None

        # dict where key is path and value is Movie instance
        # this is files which are downloading or downloaded
        self.files = None

        # piece_length in this torrent
        self.piece_length = None
        # amount of pieces which made up DOWNLOAD_PIECE_SIZE
        self._jump = None
        # if first prioritizing task was run once
        self._prioritized = False

        self.priority_interval = settings.PRIORITY_INTERVAL

        self._priority_thread_stop = Event()

        self._priority_timer = None

        self._downloading = None

    def __del__(self):
        self._stop_torrent_threads()

    def __str__(self):
        return self.name

    def bind_session(self, session):
        """
        Creates torrent handler based on source_type
        """
        add_data = {}
        if self.source_type == "TORRENT":
            add_data['ti'] = lt.torrent_info(self.source)
        elif self.source_type == "MAGNET":
            add_data['url'] = self.source
        add_data['save_path'] = self._get_download_dir()
        add_data['storage_mode'] = lt.storage_mode_t(1)
        self.torrent_handler = session.add_torrent(add_data)

        self._prioritize_to_none()

    def get_filelist(self):
        info = self.get_torrent_info(wait=True)
        return [file.path for file in info.files()]

    def get_movies_filelist(self):
        if self.files is None:
            self._create_movies()
        return list(self.files.keys())

    def get_movies(self):
        if self.files is None:
            self._create_movies()
        return list(self.files.values())

    def _create_movies(self):
        info = self.get_torrent_info()
        files = info.files()

        self.piece_length = info.piece_length()
        self.priority_interval = settings.PRIORITY_INTERVAL * self.piece_length / (
            1024 ** 2)
        self._jump = int(settings.DOWNLOAD_PIECE_SIZE / self.piece_length) + 1

        self.files = {}
        for file in files:
            ext = os.path.splitext(file.path)[1]
            if ext and ext[1:].lower() in settings.SUPPORTED_MOVIE_EXTENSIONS:
                first_piece = int(file.offset / self.piece_length)
                last_piece = int((file.size + file.offset) / self.piece_length)
                self.files[file.path] = Movie(path=file.path,
                        size=file.size, first_piece=first_piece, last_piece=last_piece,
                        piece_length=self.piece_length,
                        download_dir=self._get_download_dir())

    def download_file(self, filename:str):
        if not filename in self.get_movies_filelist():
            raise Exception("filename not found in torrent")
        self._prioritize_to_none()
        self._downloading = self.files[filename]

        if not self._priority_thread_stop or not self._priority_thread_stop.is_set():
            self._run_torrent_threads()

    def has_torrent_info(self):
        """
        Checks if torrent has downloaded metadata
        """
        try:
            self.get_torrent_info()
            return True
        except TorrentHasNotMetadataYet:
            return False

    def get_torrent_info(self, wait=False):
        """
        Gets torrent's metadata
        """
        if self._torrent_info != None:
            return self._torrent_info

        if self.torrent_handler is None:
            raise SessionNotBindedException

        if not self.torrent_handler.has_metadata():
            if wait:
                while not self.torrent_handler.has_metadata():
                    time.sleep(0.1)
            else:
                raise TorrentHasNotMetadataYet
        self._torrent_info = self.torrent_handler.get_torrent_info()
        return self._torrent_info

    def get_status(self):
        """
        Gets torrent's status with field like download rate, peers number,
        state and progress level
        """
        status = self.torrent_handler.status()
        state_str = ['queued', 'checking', 'downloading metadata',
                     'downloading', 'finished', 'seeding', 'allocating',
                     'checking fastresume']
        data = {
            'download_rate': status.download_rate,
            'num_peers': status.num_peers,
            'state': state_str[status.state],
            'progress': status.progress
        }
        return data

    def get_downloading_movie(self):
        return self._downloading

    def pause_download(self):
        self._stop_torrent_threads()
        self.torrent_handler.pause()
        self._downloading = None

    def _update_movies_progress(self):
        """
        Updates movie progress based on number of downloaded pieces
        """
        p_downloaded = self.torrent_handler.status().pieces
        movie = self.get_downloading_movie()
        first_piece, last_piece = movie.first_piece, movie.last_piece
#            logger.debug("first_piece: {}".format(first_piece))
#            logger.debug("last_piece: {}".format(last_piece ))
        counter = 0
        for item in p_downloaded[first_piece:last_piece]:
            if item == True:
                counter += 1
            else:
                break
#        logger.debug("download_pieces inside thread is: {}".format(counter))
        movie.downloaded_pieces = counter

    def _manage_pieces_priority(self):
        """
        Sets priority blocks. First pieces should be downloaded first swo its
        have the highest priority.
        """
        p_downloaded = self.torrent_handler.status().pieces
        movie = self.get_downloading_movie()
        first_piece, last_piece = movie.cur_first_piece, movie.cur_last_piece
        if not False in p_downloaded[first_piece:first_piece + self._jump + 1]:
            # all block downloaded
            first_piece += self._jump
            movie.cur_first_piece = first_piece
        # prioritezing
        # [7, 7, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ...]
        if first_piece + self._jump + self._jump <= last_piece:
            for piece in range(first_piece + 4 * self._jump,
                last_piece + 1):
#                logger.debug("the lowest priority for: {}".format(piece))
                self.torrent_handler.piece_priority(piece, 0)
        if first_piece + self._jump <= last_piece:
            for piece in range(first_piece + 2 * self._jump,
                min(last_piece + 1, first_piece + 4 * self._jump)):
#                logger.debug("low priority for: {}".format(piece))
                self.torrent_handler.piece_priority(piece, 2)
        if first_piece <= last_piece:
            for piece in range(first_piece,
                min(last_piece + 1, first_piece + 2 * self._jump)):
#                logger.debug("the highest priority for: {}".format(piece))
                self.torrent_handler.piece_priority(piece, 7)
                # for mp4 get 512KB end of file
                # TODO: bug below
            #            for piece in range(
            #                last_piece - int(self.piece_length / 512 * 1024) + 1,
            #                last_piece):
            #                logger.debug("the highest priority for (512KB end of file): {}".format(piece))
            #                self.torrent_handler.piece_priority(piece, 7)
        self._update_movies_progress()
        #if not self._priority_thread_stop.is_set():
        self._run_torrent_threads()
        #print(self.torrent_handler.piece_priorities()[key[0]:key[1]])

    def _run_torrent_threads(self):
#        logger.debug("run threads for {}".format(self.priority_interval))
        self._priority_timer = Timer(self.priority_interval,
            self._manage_pieces_priority).start()

    def _stop_torrent_threads(self):
        self._priority_thread_stop.set()
        if self._priority_timer:
            self._priority_timer.cancel()

    def _prioritize_to_none(self):
        if not self._prioritized and self.has_torrent_info():
            self._prioritized = True
            info = self.get_torrent_info()
            for piece in range(0, info.num_pieces()):
                self.torrent_handler.piece_priority(piece, 0)

    def _get_download_dir(self):
        path = os.path.join(settings.DOWNLOAD_DIR,
            hashlib.md5(self.name.encode()).hexdigest())
        try:
            os.makedirs(path)
        except OSError:
            pass
        return path


