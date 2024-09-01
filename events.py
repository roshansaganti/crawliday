"""
API Reference: https://developers.google.com/calendar/api/v3/reference#Events
"""

# import json
import logging
import time
import os
from datetime import datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
log = logging

# If modifying these scopes, delete the file token.json
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

# Variables
calendar_id = os.environ["GOOGLE_CALENDAR_ID"]


def get_credentials():
    # Get credentials for service account
    # https://github.com/googleapis/google-api-python-client/blob/main/docs/oauth.md#service-account-credentials # noqa
    return service_account.Credentials.from_service_account_file(
        "credentials.json"
    )


# Create new events
def create(movies):
    log.info("Creating events...")

    created_events = 0

    creds = get_credentials()

    # Iterate through the JSON object
    for channel in movies:
        for date in movies[channel]:
            date_to_format = datetime.strptime(
                date.replace(",", ""), "%A %B %d %Y"
            )
            movie_date = date_to_format.strftime("%Y-%m-%d")
            for movie in movies[channel][date]:
                name = movies[channel][date][movie]

                time_to_format = time.strptime(movie, "%I:%M%p")
                movie_time = time.strftime("%H:%M:%S%z", time_to_format)

                event = {
                    "summary": name,
                    "location": channel,
                    # "description": "",
                    "start": {
                        # "dateTime": "2015-05-28T09:00:00-07:00",
                        "dateTime": "{}T{}".format(movie_date, movie_time),
                        "timeZone": "America/New_York",
                    },
                    "end": {
                        "dateTime": "{}T{}".format(movie_date, movie_time),
                        "timeZone": "America/Los_Angeles",
                    },
                    # "recurrence": ["RRULE:FREQ=DAILY;COUNT=1"],
                    # "attendees": [
                    #     {"email": "lpage@example.com"},
                    #     {"email": "sbrin@example.com"},
                    # ],
                    "reminders": {
                        "useDefault": False,
                        "overrides": [
                            {"method": "popup", "minutes": 10},
                        ],
                    },
                }

                # Debugging
                # print(
                #     json.dumps(
                #         event,
                #         indent=4,
                #         ensure_ascii=False,
                #     )
                # )

                # Create event
                try:
                    service = build(
                        "calendar",
                        "v3",
                        credentials=creds,
                        cache_discovery=False,
                    )

                    # Add movies to calendar
                    event = (
                        service.events()
                        .insert(calendarId=calendar_id, body=event)
                        .execute()
                    )
                    created_events += 1
                except HttpError as error:
                    log.error(f"An error occurred: {error}")

    log.info("Created {} events".format(created_events))


def read():
    pass


def update():
    pass


def delete():
    pass


# Remove all events for the current year
def truncate():
    truncated_events = 0

    creds = get_credentials()

    date = datetime.now()

    log.info("Fetching events to truncate...")

    # Get a list of all events for the current year
    try:
        service = build(
            "calendar", "v3", credentials=creds, cache_discovery=False
        )

        # Get all events in calendar for the current year
        events = (
            service.events()
            .list(
                calendarId=calendar_id,
                timeMin="{}-01-01T00:00:00-0000".format(date.year),
                timeMax="{}-12-31T00:00:00-0000".format(date.year),
            )
            .execute()
        )
    except HttpError as error:
        log.error(f"An error occurred: {error}")

    # Check if there are events to delete
    if len(events["items"]) == 0:
        log.info("No events found")
    else:
        log.info("Found {} events".format(len(events["items"])))

        log.info("Truncating events...")

        # Delete each event
        for event in events["items"]:
            try:
                service = build(
                    "calendar", "v3", credentials=creds, cache_discovery=False
                )

                # Trucate all events in calendar
                service.events().delete(
                    calendarId=calendar_id, eventId=event["id"]
                ).execute()

                # log.info("Deleted event {}".format(event["id"]))
                truncated_events += 1
            except HttpError as error:
                log.error(f"An error occurred: {error}")

    log.info("Truncated {} events".format(truncated_events))


# Test function
def test_credentials():
    creds = get_credentials()

    # print(creds)

    # Get a list of all events for the current year
    try:
        service = build(
            "calendar", "v3", credentials=creds, cache_discovery=False
        )

        # Get all events in calendar for the current year
        events = (
            service.events()
            .list(calendarId=calendar_id, maxResults=1)
            .execute()
        )
    except HttpError as error:
        log.error(f"An error occurred: {error}")

    print(events)
