# based on:
# https://developers.google.com/calendar/api/quickstart/python

import logging
import os
import re

from datetime import datetime
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from otg.api.core import get_default_config_dir


SCOPES = ["https://www.googleapis.com/auth/calendar"]


_logger = None


def logger() -> logging.Logger:
    """
    Return the logger to use.

    :return: the logger
    :rtype: logging.Logger
    """
    global _logger
    if _logger is None:
        _logger = logging.getLogger("otg.api.google")
    return _logger


def credentials_token_path() -> str:
    """
    Returns the default token path.

    :return: the token path
    :rtype: str
    """
    return os.path.join(get_default_config_dir(), "token.json")


def load_credentials_token() -> Optional[Credentials]:
    """
    Tries to load the credentials from the token.json file.

    :return: the credentials, None if token file not available
    :rtype: Credentials
    """
    path = credentials_token_path()
    if os.path.exists(path):
        return Credentials.from_authorized_user_file(path, SCOPES)
    else:
        logger().info("Token file does not exist (yet): %s" % path)
        return None


def save_credentials_token(creds: Credentials):
    """
    Saves the credentials token JSON file.

    :param creds: the credentials to store
    :type creds: Credentials
    """
    path = credentials_token_path()
    logger().info("Saving credentials to: %s" % path)
    with open(path, "w") as token:
        token.write(creds.to_json())


def init_credentials(credentials: str, creds: Credentials = None) -> Credentials:
    """
    Initializes the credentials from the credentials JSON file.

    :param credentials: the credentials JSON file to use
    :type credentials: str
    :param creds: the credentials object to re-use, can be None
    :return: the credentials object
    :rtype: Credentials
    """
    if creds is not None:
        if not creds.valid:
            logger().info("Refreshing token...")
            creds.refresh(Request())
    else:
        logger().info("Creating token from credentials...")
        flow = InstalledAppFlow.from_client_secrets_file(credentials, SCOPES)
        creds = flow.run_local_server(port=0)
        save_credentials_token(creds)
    return creds


def init_service(credentials: str):
    """
    Initializes the calendar service instance.

    :param credentials: the credentials JSON file to use
    :type credentials: str
    :return: the service, None if failed to instantiate
    """
    creds = load_credentials_token()
    creds = init_credentials(credentials, creds)
    try:
        return build("calendar", "v3", credentials=creds)
    except HttpError as error:
        logger().error(f"An error occurred: {error}")
        return None


def filter_events(service, calendar: str, regexp_id: str = None, regexp_summary: str = None):
    """
    Filters the events from Google calendar.

    :param service: the service instance to use
    :param calendar: the name of the calendar to retrieve
    :type calendar: str
    :param regexp_id: the regular expression that the event IDs must match, ignored if None
    :type regexp_id: str
    :param regexp_summary: the regular expression that the event summaries must match, ignored if None
    :type regexp_summary: str
    :return:
    """
    result = []

    # at most 1 year's worth
    # TODO parameters?
    timeMin = datetime.utcnow().isoformat() + "Z"
    timeMax = datetime.utcnow()
    timeMax = timeMax.replace(year=timeMax.year + 1)
    timeMax = timeMax.isoformat() + "Z"

    events = (
        service.events().list(
            calendarId=calendar,
            showDeleted=True,
            timeMin=timeMin,
            timeMax=timeMax,
        ).execute()
    )

    for event in events["items"]:
        if event["status"].lower() == "cancelled":
            continue
        if regexp_id is not None:
            match = re.match(regexp_id, event["id"])
            if not match:
                continue
        if "summary" in event:
            if regexp_summary is not None:
                match = re.match(regexp_summary, event["summary"])
                if not match:
                    continue
        result.append(event)

    return result
