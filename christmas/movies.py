import requests
from bs4 import BeautifulSoup
import logging

# import json

log = logging.getLogger(__name__)

url_list = [
    "https://christmastvschedule.com/",
]


def crawl():
    output = []
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

        # Date
        output.append(showtime.find("td", class_="column-2").text)
        # Time
        output.append(showtime.find("td", class_="column-3").text)
        # Title
        output.append(showtime.find("td", class_="column-4").text)
        # Channel
        output.append(showtime.find("td", class_="column-5").text)

        output.append("\n\n")

        # Parse showtimes into dictionary
        movies.append(
            {
                "date": date,
                "time": time,
                "title": title,
                "channel": channel,
            }
        )

    # Store output to file
    with open("output.txt", mode="wt", encoding="utf-8") as f:
        f.write("\n".join(output))

    return 0, movies
