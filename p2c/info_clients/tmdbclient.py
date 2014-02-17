# -*- coding: utf-8 -*-
import json
import logging
import requests
from p2c import secret

logger = logging.getLogger(__name__)

class TMDBApiClient(object):
    URL = "http://api.themoviedb.org/3/"
    params = {'api_key': secret.TMDB_API_KEY}

    def __init__(self):
        super().__init__()
        url = self.URL + "configuration"
        configuration = json.loads(requests.get(url, params=self.params).text)
        self.base_url = configuration['images']['base_url'] + configuration['images']['poster_sizes'][1]

    def search_for_movies(self, title):
        url = self.URL + "search/movie"
        params = self.params.copy()
        params.update({"query": title})
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = json.loads(response.text)
            return data['results']
        else:
            logger.info("TMBD responsed with %s" % response.status_code)
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
