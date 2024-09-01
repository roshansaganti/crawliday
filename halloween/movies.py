import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime

# import json

log = logging.getLogger(__name__)

url_list = [
    "https://www.halloweenmoviesontv.com/turner-classic-movies-october-horror/",  # noqa
    "https://www.halloweenmoviesontv.com/syfy-31-days-of-halloween/",
    "https://www.halloweenmoviesontv.com/abc-family-13-nights-of-halloween-schedule/",  # noqa
    "https://www.halloweenmoviesontv.com/metv-svengoolies-halloween-boonanza/",
    "https://www.halloweenmoviesontv.com/movies-friday-night-frights/",
]


def crawl():
    # Variables
    movies = {}
    year = datetime.now().year

    for url in url_list:
        # Get channel name
        if url == url_list[0]:
            channel = "Turner Classic Movies (TCM)"
        elif url == url_list[1]:
            channel = "Syfy"
        elif url == url_list[2]:
            channel = "Freeform"
        elif url == url_list[3]:
            channel = "MeTV"
        elif url == url_list[4]:
            channel = "Movies! TV Network"

        try:
            r = requests.get(url)
            r.raise_for_status()
        except Exception as e:
            log.info(e)
            return 1

        soup = BeautifulSoup(r.content, "html.parser")

        dates = soup.find(class_="cm-entry-summary").findAll("p")

        # Iterate through the dates
        for date in dates:
            if str(year) in date.text and date.strong:
                # [1:-1] will remove the first and last items
                listings = date.find_next_siblings()[0].text[1:-1].split("\n")

                # Iterate through the movie listings
                for listing in listings:
                    ticket = listing.split("–")

                    if len(ticket) == 2:
                        if (
                            ticket[0].find("am") != -1
                            or ticket[0].find("pm") != -1
                        ):
                            time = ticket[0].strip()
                        else:
                            break
                        name = ticket[1].strip()

                    # If channel exists, just add new key value pairs
                    if channel in movies:
                        # If date exists, just add new key value pairs
                        if date.text in movies[channel]:
                            movies[channel][date.text][time] = name
                        # If date does NOT exist, create empty dictionaries
                        else:
                            movies[channel][date.text] = {}
                            movies[channel][date.text][time] = name
                    # If channel does NOT exist, create empty dictionaries
                    else:
                        movies[channel] = {}
                        movies[channel][date.text] = {}
                        movies[channel][date.text][time] = name

    # Debugging
    # print(
    #     json.dumps(
    #         movies,
    #         indent=4,
    #         # https://stackoverflow.com/questions/18337407/saving-utf-8-texts-with-json-dumps-as-utf-8-not-as-a-u-escape-sequence # noqa
    #         ensure_ascii=False,
    #     )
    # )

    return 0, movies
