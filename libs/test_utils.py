# -*- coding: utf-8 -*-
from http.server import SimpleHTTPRequestHandler
import urllib.parse
from os import path
import os
from p2c import settings

class TestSimpleHTTPRequestHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = posixpath.normpath(urllib.parse.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = os.path.normpath(settings.TEST_DIR)
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path