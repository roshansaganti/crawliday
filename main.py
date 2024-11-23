import sys
import logging
import halloween.movies as halloween_movies
import christmas.movies as christmas_movies

import events

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
log = logging


halloween_crawler = halloween_movies
christmas_crawler = christmas_movies


def store_movies(movies):
    # events.test_credentials()
    events.truncate()
    events.create(movies)


def crawl_christmas():
    log.info("Crawling Christmas movies...")

    # Crawl for Christmas Movies
    status, movies = christmas_movies.crawl()

    if status == 0:
        log.info("Christmas movie schedule crawl complete!")
        # store_movies(movies)
    else:
        log.info("Error. Something went wrong.")


def crawl_halloween():
    log.info("Crawling Halloween movies...")

    # Crawl for Halloween Movies
    status, movies = halloween_movies.crawl()

    if status == 0:
        log.info("Halloween movie schedule crawl complete!")
        store_movies(movies)
    else:
        log.info("Error. Something went wrong.")
        return


if __name__ == "__main__":
    if sys.argv[1] == "halloween":
        crawl_halloween()
    elif sys.argv[1] == "christmas":
        crawl_christmas()
