import re
import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import json

log = logging.getLogger(__name__)

url_list = [
    "https://www.halloweenmoviesontv.com/turner-classic-movies-october-horror/",
    "https://www.halloweenmoviesontv.com/syfy-31-days-of-halloween/",
    "https://www.halloweenmoviesontv.com/abc-family-13-nights-of-halloween-schedule/",
    "https://www.halloweenmoviesontv.com/metv-svengoolies-halloween-boonanza/",
    "https://www.halloweenmoviesontv.com/movies-friday-night-frights/",
]


def crawl():
    movies = {}

    try:
        r = requests.get(url_list[4])
        r.raise_for_status()
    except Exception as e:
        log.info(e)
        return

    soup = BeautifulSoup(r.content, "html.parser")

    test = soup.find(class_="cm-entry-summary").findAll("p")

    test = [element for i, element in enumerate(test) if i not in [0, 1, 2, 3, 7]]

    for item in test:
        if item.strong:
            time = item.find_next("li").text

            movies[item.text] = []
            movies[item.text].append(time)

    # TODO: Set up Google Calendar Integration

    # TODO: Add movies to Google Calendar
    # for date in movies.keys():
    #     print(date)
    #     for movie in movies[date]:
    #         print(movie)

    print(
        json.dumps(
            movies,
            indent=4,
            # https://stackoverflow.com/questions/18337407/saving-utf-8-texts-with-json-dumps-as-utf-8-not-as-a-u-escape-sequence
            ensure_ascii=False
        )
    )
