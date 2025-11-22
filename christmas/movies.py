import requests
from bs4 import BeautifulSoup
import logging

# import json

log = logging.getLogger(__name__)

url_list = [
    "https://christmastvschedule.com/",
]


def crawl():
    movies = []

    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",  # noqa
    }

    try:
        r = requests.get(url_list[0], headers=headers)
        r.raise_for_status()
    except Exception as e:
        log.info(e)
        return

    soup = BeautifulSoup(r.content, "html.parser")

    # Get all showtime
    showtimes = soup.find("tbody").findAll("tr")

    for showtime in showtimes:
        date = showtime.find("td", class_="column-2").text
        time = showtime.find("td", class_="column-3").text
        title = showtime.find("td", class_="column-4").text
        channel = showtime.find("td", class_="column-5").text

        # Parse showtimes into dictionary
        if (
            not date == ""
            or not time == ""
            or not title == ""
            or not channel == ""
        ):
            movies.append(
                {
                    "date": date,
                    "time": time,
                    "title": title,
                    "channel": channel,
                }
            )

    print(movies)

    return 0, movies
