"""
API Reference: https://developers.google.com/calendar/api/v3/reference#Events
"""

import logging
import json
import time
import os.path
from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
log = logging

# If modifying these scopes, delete the file token.json
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

# Variables
calendar_id = "67527d508ed63b7e7362a0ea43a2d28a8ffc4983ecf413e7c7f302306694f4bd@group.calendar.google.com"


def get_credentials():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


# Create new events
def create(movies):
    creds = get_credentials()

    # Iterate through the JSON object
    for channel in movies:
        for date in movies[channel]:
            date_to_format = datetime.strptime(date, "%A, %B %d, %Y")
            movie_date = date_to_format.strftime("%Y-%m-%d")
            for movie in movies[channel][date]:
                name = movies[channel][date][movie]

                time_to_format = time.strptime(movie, "%I:%M%p")
                movie_time = time.strftime("%H:%M:%S%z", time_to_format)

                event = {
                    "summary": name,
                    "location": channel,
                    # "description": "A chance to hear more about Google's developer products.",
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
                #         # https://stackoverflow.com/questions/18337407/saving-utf-8-texts-with-json-dumps-as-utf-8-not-as-a-u-escape-sequence
                #         ensure_ascii=False,
                #     )
                # )

                # Create event
                try:
                    service = build("calendar", "v3", credentials=creds)

                    # Add movies to calendar
                    event = (
                        service.events()
                        .insert(calendarId=calendar_id, body=event)
                        .execute()
                    )
                    log.info("Created event {}".format(event["id"]))
                except HttpError as error:
                    log.info(f"An error occurred: {error}")

    log.info("Creation complete")


def read():
    pass


def update():
    pass


def delete():
    pass


# Remove all events for the current year
def truncate():
    creds = get_credentials()

    date = datetime.now()

    log.info("Fetching events to truncate...")

    # Get a list of all events for the current year
    try:
        service = build("calendar", "v3", credentials=creds)

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

        # Delete each event
        for event in events["items"]:
            try:
                service = build("calendar", "v3", credentials=creds)

                # Trucate all events in calendar
                service.events().delete(
                    calendarId=calendar_id, eventId=event["id"]
                ).execute()

                log.info("Deleted event {}".format(event["id"]))
            except HttpError as error:
                log.info(f"An error occurred: {error}")

    log.info("Truncation complete")
