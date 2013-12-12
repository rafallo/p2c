# -*- coding: utf-8 -*-
import os

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..")

DOWNLOAD_DIR = os.path.join(PROJECT_ROOT, "tmp")

TEST_DIR = os.path.join(PROJECT_ROOT, "test_data")

STORAGE_PATH = os.path.join(PROJECT_ROOT, "tmp", "configuration.json")

START_PORT = 6821
END_PORT = 6831

SUPPORTED_MOVIE_EXTENSIONS = (
"mp4", "avi", "mkv", "ogv", "ogg", "mpeg", "flv", "wmv")
SUPPORTED_SUBTITLE_EXTENSIONS = ("txt", "srt")

DOWNLOAD_PIECE_SIZE = 1024 * 1024 * 5

# for 1MB piece length
PRIORITY_INTERVAL = 0.2