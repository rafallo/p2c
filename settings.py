# -*- coding: utf-8 -*-
import os, tempfile

PROJECT_ROOT = os.path.dirname(__file__)

TMP_DIR = tempfile.mkdtemp()

DOWNLOAD_DIR = os.path.join(TMP_DIR, "download")

LOG_DIR = os.path.join(TMP_DIR, "logs")

try:
    os.makedirs(DOWNLOAD_DIR)
except OSError:
    pass

try:
    os.makedirs(LOG_DIR)
except OSError:
    pass

TEST_DIR = os.path.join(PROJECT_ROOT, "test_data")

try:
    os.makedirs(TEST_DIR)
except OSError:
    pass

STORAGE_PATH = os.path.join(TMP_DIR, "download", "configuration.json")

START_PORT = 6841
END_PORT = 6851

SUPPORTED_MOVIE_EXTENSIONS = (
"mp4", "avi", "mkv", "ogv", "ogg", "mpeg", "flv", "wmv")
SUPPORTED_SUBTITLE_EXTENSIONS = ("txt", "srt")

DOWNLOAD_PIECE_SIZE = 1024 * 1024 * 5

# for 1MB piece length
PRIORITY_INTERVAL = 2