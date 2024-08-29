[![bump-version](https://github.com/roshansaganti/crawliday/actions/workflows/bump-version.yml/badge.svg)](https://github.com/roshansaganti/crawliday/actions/workflows/bump-version.yml)
[![build](https://github.com/roshansaganti/crawliday/actions/workflows/build.yml/badge.svg)](https://github.com/roshansaganti/crawliday/actions/workflows/build.yml)

# Crawliday

Crawl websites for holiday-themed movies like Halloween and Christmas and then add them to a Google Calendar.

## Clone the project

## Setup Python Environment

The following command will create a new Python environment using the Pipfile.lock

```
pipenv sync
```

## Setting Up Your Google Calendar

### Create a Google Calendar

How to create a Google Calendar:
https://support.google.com/calendar/answer/37095?hl=en

### Find Your Calendar's ID

Create a new `.env` file in your root directory and populate it like so:

```
GOOGLE_CALENDAR_ID={{ CALENDAR_ID }}
```

### Authentication

There are two methods to authenticate to your Google Calendar:

1. OAuth
2. Service Account

For this project, I've decided to use a `service account` as this will allow the application to operate with no user intervention.

**Note:** Although the option exists, Google does **not** recommend the use of `API Keys` to authenticate to `Google Calendar API`.

#### OAuth Consent

#### Google Cloud Service Account

Download your credentials JSON file from Google Cloud. Your credentials file will look like this:

```
{
  "type": "service_account",
  "project_id": "***",
  "private_key_id": "***",
  "private_key": "-----BEGIN PRIVATE KEY-----\n-----END PRIVATE KEY-----\n",
  "client_email": "***",
  "client_id": "***",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/***",
  "universe_domain": "googleapis.com"
}
```

Save your credentials as `credentials.json` and store it into the root of the project.

## Run program

```
python crawl.py {{ ARG }}
```

### Available Arguments

`halloween` - For fetching Halloween movies

`christmas` - For fetching Christmas movies

## Running Unit Tests

Run the following command in the root of the directory:

```
python -m unittest discover
```

All tests are located in the `tests/` directory
