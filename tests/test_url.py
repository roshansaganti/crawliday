import unittest

# Halloween imports
from halloween import movies as hm

# Christmas imports
# from christmas import movies as cm

# Google Cloud imports
import events
from google.oauth2 import service_account


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


# Test Google Cloud
class TestGoogleCloud(unittest.TestCase):
    # Test Google Cloud Service Account Credentials
    def test_get_credentials(self):
        creds = events.get_credentials()

        # Assertions
        self.assertIsInstance(creds, service_account.Credentials)


if __name__ == "__main__":
    unittest.main()
