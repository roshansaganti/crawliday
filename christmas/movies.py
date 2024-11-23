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
    movies = {}

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

    # Remove all 'span' tags from the HTML
    for s in soup(["span"]):
        s.extract()

    # print(spans)

    # for span in spans:
    #     print(span.text)

    # Get all dates
    dates = soup.find(class_="czr-wp-the-content").findAll("h3")
    # showtimes = soup.find(class_="czr-wp-the-content").findAll("p")
    # showtimes = soup.find(class_="czr-wp-the-content").findAll("li")

    # print(len(dates))

    # Remove header text
    dates.pop(0)

    # print(dates)

    # Remove empty items
    # for x in soup.find_all():
    #     print((x.text))
    #     # print(len(x.b.text))
    #     if len(x.get_text(strip=True)) == 0:
    #         print("yes")
    #         print(x.text)
    #         x.extract()

    for date in dates:
        # print(date)

        # if date.b.text == "":
        #     dates.remove(date)

        # print(date.b.text)

        # if date.b.find_next_sibling():
        #     print("DELETE BELOW")
        #     print(date.b.find_next_sibling())
        #     print("DELETE ABOVE")
        # dates.remove(date.b.span.text)

        output.append(date.b.text)

        # lines = date.get_text().strip().splitlines()
        # if len(lines) > 1:
        #     for line in lines:

        #         temp_date = ""
        #         temp_time = ""
        #         # Showtime
        #         if re.search(r"am|pm ", line):
        #             if line[0].isdigit():
        #                 temp_time = line
        #                 # times.append(line)
        #                 pass
        #                 # print(line)
        #                 # print("this is a showtime")
        #         # Date
        #         elif re.search(r",", line):
        #             temp_date = line
        #             pass
        #             # print(line)
        #             # print("this is a date")

        #         # print(temp_date)
        #         # print(temp_time)

        #         # TODO: Store into JSON object
        #         if not temp_date == "" and not temp_time == "":
        #             movies[temp_date] = temp_time

        # print(movies)

        # print("INCREMENT DATE")

    # showtimes = json.loads(showtimes)
    # print(json.dumps(showtimes, indent=4))
    # print(showtimes[13])
    # print(movies)

    # Store output to file
    with open("output.txt", mode="wt", encoding="utf-8") as f:
        f.write("\n".join(output))

    return 0, movies
