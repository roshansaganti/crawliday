import sys
import requests
from bs4 import BeautifulSoup
import logging
import halloween.movies as halloween_movies
import christmas.movies as christmas_movies

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
log = logging


halloween_crawler = halloween_movies
christmas_crawler = christmas_movies


def crawl_christmas():
    # Crawl for Christmas Movies
    status_code = christmas_movies.crawl()

    if status_code is 0:
        log.info("Christmas movie schedule crawl complete!")
    else:
        log.info("Error. Something went wrong.")


def crawl_halloween():
    # Crawl for Halloween Movies
    status_code = halloween_movies.crawl()

    if status_code is 0:
        log.info("Halloween movie schedule crawl complete!")
    else:
        log.info("Error. Something went wrong.")


if __name__ == "__main__":
    if sys.argv[1] == "halloween":
        crawl_halloween()
    elif sys.argv[1] == "christmas":
        crawl_christmas()
