import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json
# SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

# Variables
# calendar_id = "67527d508ed63b7e7362a0ea43a2d28a8ffc4983ecf413e7c7f302306694f4bd@group.calendar.google.com"
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

    event = {
        "summary": "Google I/O 2015",
        "location": "800 Howard St., San Francisco, CA 94103",
        "description": "A chance to hear more about Google's developer products.",
        "start": {
            "dateTime": "2015-05-28T09:00:00-07:00",
            "timeZone": "America/Los_Angeles",
        },
        "end": {
            "dateTime": "2015-05-28T17:00:00-07:00",
            "timeZone": "America/Los_Angeles",
        },
        "recurrence": ["RRULE:FREQ=DAILY;COUNT=1"],
        "attendees": [
            {"email": "lpage@example.com"},
            {"email": "sbrin@example.com"},
        ],
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
        event = service.events().insert(calendarId=calendar_id, body=event).execute()

    except HttpError as error:
        print(f"An error occurred: {error}")


def read():
    pass


def update():
    pass


def delete():
    pass
