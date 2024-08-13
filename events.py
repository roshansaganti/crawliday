import time
import os.path
from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

# Variables
calendar_id = "fd973e69753e0730ef2ff2627ab0e983fce4944c220d7c39e4469031743bc764@group.calendar.google.com"


def create(movies):
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

    for date in movies:
        date_to_format = datetime.strptime(date, "%A, %B %d, %Y")
        movie_date = date_to_format.strftime("%Y-%m-%d")
        for movie in movies[date]:
            name = movies[date][movie]

            time_to_format = time.strptime(movie, "%I:%M%p")
            movie_time = time.strftime("%H:%M:%S%z", time_to_format)

            event = {
                "summary": name,
                # "location": "800 Howard St., San Francisco, CA 94103",
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
                        {"method": "email", "minutes": 24 * 60},
                        {"method": "popup", "minutes": 10},
                    ],
                },
            }

            try:
                service = build("calendar", "v3", credentials=creds)

                # Add movies to calendar
                event = (
                    service.events()
                    .insert(calendarId=calendar_id, body=event)
                    .execute()
                )

            except HttpError as error:
                print(f"An error occurred: {error}")


def read():
    pass


def update():
    pass


def delete():
    pass
