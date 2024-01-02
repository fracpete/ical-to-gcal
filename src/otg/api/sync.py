import json
import logging
import traceback

from datetime import datetime
from typing import List, Dict, Any

import icalendar

from googleapiclient.errors import HttpError
from otg.api.events import EVENT_ID, EVENT_SUMMARY, EVENT_DESCRIPTION, EVENT_LOCATION, EVENT_RECURRENCE, EVENT_STATUS, EVENT_START, EVENT_END, EVENT_UPDATED
from otg.api.events import event_field, is_same_event, has_event_changed


ACTION_ADD = "add"
ACTION_DELETE = "delete"
ACTION_UPDATE = "update"
ACTIONS = [
    ACTION_ADD,
    ACTION_DELETE,
    ACTION_UPDATE,
]


_logger = None


def logger() -> logging.Logger:
    """
    Return the logger to use.

    :return: the logger
    :rtype: logging.Logger
    """
    global _logger
    if _logger is None:
        _logger = logging.getLogger("otg.api.sync")
    return _logger


def compare(outlook_events: List, google_events: List) -> Dict[str, List[Any]]:
    """
    Compares the Outlook and Google events and returns a dictionary with
    add/delete/update lists of events.

    :param outlook_events: the outlook events to use in the comparison
    :type outlook_events: list
    :param google_events: the google events to use in the comparsion
    :type google_events: list
    :return: the action dictionary
    :rtype: dict
    """
    result = dict()

    for oevent in outlook_events:
        found = False
        for gevent in google_events:
            if is_same_event(oevent, gevent):
                found = True
                if has_event_changed(oevent, gevent):
                    if ACTION_UPDATE not in result:
                        result[ACTION_UPDATE] = []
                    result[ACTION_UPDATE].append((oevent, gevent))
        if not found:
            if ACTION_ADD not in result:
                result[ACTION_ADD] = []
            result[ACTION_ADD].append(oevent)

    for gevent in google_events:
        found = False
        for oevent in outlook_events:
            if is_same_event(oevent, gevent):
                found = True
        if not found:
            if ACTION_DELETE not in result:
                result[ACTION_DELETE] = []
            result[ACTION_DELETE].append(gevent)

    return result


def add_event(service, gcalendar: str, oevent, dry_run: bool = False) -> bool:
    """
    Adds the Outlook event in the Google calendar.

    :param service: the Google Calendar service instance to use
    :param gcalendar: the Google Calendar to use
    :type gcalendar: str
    :param oevent: the Outlook event to add
    :type oevent: icalendar.Event
    :param dry_run: whether to perform a dry-run only and not change the Google Calendar at all
    :type dry_run: bool
    :return: True if successfully added
    :rtype: bool
    """
    logger().info("adding: %s" % event_field(oevent, EVENT_ID))
    body = {
        "summary": event_field(oevent, EVENT_SUMMARY),
        "iCalUID": event_field(oevent, EVENT_ID),
        "reminders": {"useDefaults": True},
    }
    if event_field(oevent, EVENT_LOCATION) is not None:
        body["location"] = event_field(oevent, EVENT_LOCATION)
    if event_field(oevent, EVENT_STATUS) is not None:
        body["status"] = event_field(oevent, EVENT_STATUS).lower()
    if event_field(oevent, EVENT_DESCRIPTION) is not None:
        body["description"] = event_field(oevent, EVENT_DESCRIPTION)
    start = event_field(oevent, EVENT_START)
    end = event_field(oevent, EVENT_END)
    if (start is not None) and (end is not None):
        if isinstance(start, datetime):
            body["start"] = {"dateTime": start.isoformat(), "timeZone": str(start.tzinfo)}
            body["end"] = {"dateTime": end.isoformat(), "timeZone": str(end.tzinfo)}
        else:
            body["start"] = {"date": start.strftime("%Y-%m-%d")}
            body["end"] = {"date": end.strftime("%Y-%m-%d")}
    if event_field(oevent, EVENT_RECURRENCE) is not None:
        body["recurrence"] = ["RRULE:" + event_field(oevent, EVENT_RECURRENCE).to_ical().decode()]

    if dry_run:
        logger().info("add body:\n%s" % (json.dumps(body, indent=2)))
    else:
        try:
            event = (
                service.events().insert(
                    calendarId=gcalendar,
                    body=body,
                ).execute()
            )
            logger().info("event added: %s" % str(event))
            return True
        except HttpError as error:
            logger().error("Failed to add (cal=%s): %s" % (gcalendar, str(oevent)), exc_info=True)
            return False


def delete_event(service, gcalendar: str, gevent, dry_run: bool = False) -> bool:
    """
    Removes the Google event in the Google calendar.

    :param service: the Google Calendar service instance to use
    :param gcalendar: the Google Calendar to use
    :type gcalendar: str
    :param gevent: the Google event to delete
    :param dry_run: whether to perform a dry-run only and not change the Google Calendar at all
    :type dry_run: bool
    :return: True if successfully deleted
    :rtype: bool
    """
    logger().info("deleting: %s" % event_field(gevent, EVENT_ID))
    if dry_run:
        return True
    else:
        try:
            (
                service.events().delete(
                    calendarId=gcalendar,
                    eventId=gevent["id"],
                ).execute()
            )
            return True
        except:
            logger().error("Failed to delete (cal=%s): %s" % (gcalendar, str(gevent)))
            return False


def update_event(service, gcalendar: str, oevent, gevent, dry_run: bool = False) -> bool:
    """
    Updates the Outlook event in the Google calendar.

    :param service: the Google Calendar service instance to use
    :param gcalendar: the Google Calendar to use
    :type gcalendar: str
    :param oevent: the Outlook event to update
    :type oevent: icalendar.Event
    :param gevent: the corresponding Google calendar event
    :param dry_run: whether to perform a dry-run only and not change the Google Calendar at all
    :type dry_run: bool
    :return: True if successfully updated
    :rtype: bool
    """
    if gevent is None:
        logger().info("updating %s" % event_field(oevent, EVENT_ID))
    else:
        logger().info("updating %s with %s" % (event_field(gevent, EVENT_ID), event_field(oevent, EVENT_ID)))
    body = {
        "summary": event_field(oevent, EVENT_SUMMARY),
        "iCalUID": event_field(oevent, EVENT_ID),
        "reminders": {"useDefaults": True},
    }
    if event_field(oevent, EVENT_LOCATION) is not None:
        body["location"] = event_field(oevent, EVENT_LOCATION)
    if event_field(oevent, EVENT_STATUS) is not None:
        body["status"] = event_field(oevent, EVENT_STATUS).lower()
    if event_field(oevent, EVENT_DESCRIPTION) is not None:
        body["description"] = event_field(oevent, EVENT_DESCRIPTION)
    start = event_field(oevent, EVENT_START)
    end = event_field(oevent, EVENT_END)
    if (start is not None) and (end is not None):
        if isinstance(start, datetime):
            body["start"] = {"dateTime": start.isoformat(), "timeZone": str(start.tzinfo)}
            body["end"] = {"dateTime": end.isoformat(), "timeZone": str(end.tzinfo)}
        else:
            body["start"] = {"date": start.strftime("%Y-%m-%d")}
            body["end"] = {"date": end.strftime("%Y-%m-%d")}
    if event_field(oevent, EVENT_RECURRENCE) is not None:
        body["recurrence"] = ["RRULE:" + event_field(oevent, EVENT_RECURRENCE).to_ical().decode()]

    if dry_run:
        logger().info("update body:\n%s" % (json.dumps(body, indent=2)))
    else:
        try:
            event = (
                service.events().update(
                    calendarId=gcalendar,
                    eventId=event_field(gevent, EVENT_ID),
                    body=body,
                ).execute()
            )
            logger().info("event updated: %s" % str(event))
            return True
        except:
            logger().error("Failed to update (cal=%s): %s" % (gcalendar, str(oevent)), exc_info=True)
            return False


def sync(service, gcalendar: str, actions: Dict[str, List], dry_run: bool = False) -> Dict[str, List[Any]]:
    """
    Performs the sync.

    :param service: the Google Calendar service instance to use
    :param gcalendar: the Google Calendar to use
    :type gcalendar: str
    :param actions: the dictionary with the add/delete/update event lists
    :type actions: dict
    :param dry_run: whether to perform a dry-run only and not change the Google Calendar at all
    :type dry_run: bool
    :return: the dictionary with events per action that failed: action -> list of tuples; with last element in tuple the exception string
    :rtype: dict
    """
    result = dict()
    for action in ACTIONS:
        result[action] = []

    for action in actions:
        if action == ACTION_ADD:
            for oevent in actions[action]:
                try:
                    logger().info("adding: %s" % str(oevent))
                    add_event(service, gcalendar, oevent, dry_run=dry_run)
                except:
                    result[action].append((oevent, traceback.format_exc()))
        elif action == ACTION_UPDATE:
            for oevent, gevent in actions[action]:
                try:
                    logger().info("updating: %s -> %s" % (str(oevent), str(gevent)))
                    update_event(service, gcalendar, oevent, gevent, dry_run=dry_run)
                except:
                    result[action].append((oevent, gevent, traceback.format_exc()))
        elif action == ACTION_DELETE:
            for gevent in actions[action]:
                try:
                    logger().info("deleting: %s" % str(gevent))
                    delete_event(service, gcalendar, gevent, dry_run=dry_run)
                except:
                    result[action].append((gevent, traceback.format_exc()))

    for action in ACTIONS:
        if len(result[action]) == 0:
            del result[action]

    return result
