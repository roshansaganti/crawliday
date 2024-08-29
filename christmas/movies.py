import re
import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime

# import json

log = logging.getLogger(__name__)

url_list = [
    "https://christmastvschedule.com/",
]


def crawl():
    # dates = []
    # movie_times = []
    # movie_titles = []

    movies = {}

    # dates = []
    # times = []

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

    # print(
    #     soup.find(class_="czr-wp-the-content")
    #     .findAll("ul")[0]
    #     # .string.split(" ")[0]
    #     # .strip()
    #     )

    # Get year of schedule
    year = soup.find(class_="czr-title").string.split(" ")[0].strip()

    # Validate current year match
    if int(year) == datetime.now().year:
        log.info("Correct year! Proceeding!")
        # return 0
    else:
        log.error("Incorrect year! Quitting!")
        return 1

    # Get all dates
    schedule = soup.find(class_="czr-wp-the-content").findAll("p")
    # showtimes = soup.find(class_="czr-wp-the-content").findAll("li")

    # print(schedule[3])

    # temp_date = ""
    # temp_time = ""

    for date in schedule:
        # print(date.b)
        # print(date.get_text())
        # print(date.span)

        lines = date.get_text().strip().splitlines()
        if len(lines) > 1:
            for line in lines:

                temp_date = ""
                temp_time = ""
                # Showtime
                if re.search(r"am|pm ", line):
                    if line[0].isdigit():
                        temp_time = line
                        # times.append(line)
                        pass
                        # print(line)
                        # print("this is a showtime")
                # Date
                elif re.search(r",", line):
                    temp_date = line
                    pass
                    # print(line)
                    # print("this is a date")

                # print(temp_date)
                # print(temp_time)

                # TODO: Store into JSON object
                if not temp_date == "" and not temp_time == "":
                    movies[temp_date] = temp_time

                print(movies)

        # print("INCREMENT DATE")

    # showtimes = json.loads(showtimes)
    # print(json.dumps(showtimes, indent=4))
    # print(showtimes[13])
    print(movies)
