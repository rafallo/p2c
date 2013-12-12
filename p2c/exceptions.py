# -*- coding: utf-8 -*-

class SessionNotBindedException(Exception):
    pass

class TorrentHasNotMetadataYet(Exception):
    pass

class NotDownloadingException(Exception):
    pass