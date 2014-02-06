# -*- coding: utf-8 -*-
from unittest import TestCase
from p2c.info_clients.omdbclient import OMDBApiClient
from p2c.info_clients.tmdbclient import TMDBApiClient

class OMDBApiClientTestCase(TestCase):
    def setUp(self):
        self.client = OMDBApiClient()

    def test_get_movie_info(self):
        movie = self.client.get_movie_info("the matrix")
        self.assertEqual(movie['Title'], "The Matrix")
        self.assertEqual(movie['Year'], "1999")

    def test_search_for_movie(self):
        movies = self.client.search_for_movies("matrix")
        candidate = movies[0]
        self.assertEqual(candidate['Title'], "The Matrix")

    def test_search_for_movie_fail(self):
        movies = self.client.search_for_movies("this movie does not exist")
        self.assertEqual(len(movies),0)

    def test_search_for_movie_info(self):
        movie = self.client.search_for_movie_info("matrix")
        self.assertEqual(movie['Title'], "The Matrix")
        self.assertEqual(movie['Year'], "1999")

    def test_match_title(self):
        movie = self.client.match_title('American.Hustle')
        self.assertEqual(movie['Title'], "American Hustle")

        movie = self.client.match_title('American Hustle (2013) XViD (Screener) DD2.0 Custom NLsubs NLtop')
        self.assertEqual(movie['Title'], "American Hustle")

class TMDBApiClientTestCase(TestCase):
    def setUp(self):
        self.client = TMDBApiClient()

    def test_search_for_movie(self):
        movies = self.client.search_for_movies("matrix")
        candidate = movies[0]
        self.assertEqual(candidate['title'], "The Matrix")
        self.assertTrue('poster_path' in candidate)

    def test_search_for_movie_fail(self):
        movies = self.client.search_for_movies("this movie does not exist")
        self.assertEqual(len(movies),0)
#
    def test_match_title(self):
        movie = self.client.match_title('American.Hustle')
        self.assertEqual(movie['title'], "American Hustle")

        movie = self.client.match_title('American Hustle (2013) XViD (Screener) DD2.0 Custom NLsubs NLtop')
        self.assertEqual(movie['title'], "American Hustle")
