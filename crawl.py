import sys
import logging
import halloween.movies as halloween_movies
import christmas.movies as christmas_movies

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
log = logging


halloween_crawler = halloween_movies
christmas_crawler = christmas_movies

def store_movies(movies):
    pass


def crawl_christmas():
    # Crawl for Christmas Movies
    status = christmas_movies.crawl()

    if status is 0:
        log.info("Christmas movie schedule crawl complete!")
    else:
        log.info("Error. Something went wrong.")


def crawl_halloween():
    # Crawl for Halloween Movies
    status, movies = halloween_movies.crawl()

    if status is 0:
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
