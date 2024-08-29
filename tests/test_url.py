import unittest

# import requests
from halloween import movies as hm


# Test Halloween MoviesS
class TestHalloween(unittest.TestCase):
    # Test Halloween movies are crawlable
    def test_crawl(self):
        status, movies = hm.crawl()

        # Assertions
        self.assertEqual(status, 0)
        self.assertIsInstance(movies, dict)


# Test Christmas movies
class TestChristmas(unittest.TestCase):
    def test_crawl(self):
        pass


if __name__ == "__main__":
    unittest.main()
