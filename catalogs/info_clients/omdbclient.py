# -*- coding: utf-8 -*-
import json
import logging
import requests

logger = logging.getLogger(__name__)

class OMDBApiClient(object):
    URL = "http://www.omdbapi.com/"

    def get_movie_info(self, title=None, id=None):
        assert(title or id)
        params = {}
        if not title is None:
            params['t'] = title
        if not id is None:
            params['i'] = id

        text = requests.get(self.URL, params=params).text
        return json.loads(text)

    def search_for_movies(self, title):
        text = requests.get(self.URL, params={'s':title}).text
        data = json.loads(text)
        if 'Search' in data:
            return data['Search']
        return []

    def match_title(self, title):
        candidates = self.search_for_movies(title)
        logger.debug("---TITLE MATCHING---")
        logger.debug("Trying %s" % title)
        if candidates:
            return candidates[0]

        candidates = self.search_for_movies(" ".join(title.split(".")))
        logger.debug("Trying %s" % " ".join(title.split(".")))
        if candidates:
            return candidates[0]

        parts = []
        for part in title.split("."):
            parts.extend(part.split(" "))

        for i in range(len(parts)-1, 1, -1):
            candidates = self.search_for_movies(" ".join(parts[:i]))
            logger.debug("Trying %s" % " ".join(parts[:i]))
            if candidates:
                return candidates[0]

    def search_for_movie_info(self, title):
        candidate = self.match_title(title)
        if candidate:
            return self.get_movie_info(id=candidate['imdbID'])