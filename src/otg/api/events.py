import logging

from datetime import datetime, date
from typing import Optional, Union, Tuple, List, Any

import icalendar


EVENT_ID = "id"
EVENT_SUMMARY = "summary"
EVENT_DESCRIPTION = "description"
EVENT_LOCATION = "location"
EVENT_STATUS = "status"
EVENT_RECURRENCE = "recurrence"
EVENT_START = "start"
EVENT_END = "end"
EVENT_UPDATED = "updated"
EVENT_ICALUID = "icaluid"

EVENT_FIELDS = [
    EVENT_ID,
    EVENT_SUMMARY,
    EVENT_LOCATION,
    EVENT_DESCRIPTION,
    EVENT_STATUS,
    EVENT_RECURRENCE,
    EVENT_START,
    EVENT_END,
    EVENT_UPDATED,
    EVENT_ICALUID,
]

EVENT_COMPARISON_FIELDS = [
    EVENT_SUMMARY,
    EVENT_DESCRIPTION,
    EVENT_LOCATION,
    EVENT_START,
    EVENT_END,
    EVENT_UPDATED,
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
        _logger = logging.getLogger("otg.api.events")
    return _logger


def event_field(event, field: str) -> Optional[Union[str, object, datetime, date]]:
    """
    Returns the specified event value.

    :param event: the event to get the value fromm
    :param field: the name of the field to retrieve
    :type field: str
    :return: the value, can be None; summary/description is empty string when missing; start/end are returned as datetime objects
    """
    if field not in EVENT_FIELDS:
        raise Exception("Unknown event field: %s" % field)

    if isinstance(event, icalendar.Event):
        if (field == EVENT_ID) or (field == EVENT_ICALUID):
            return event["UID"]
        elif field == EVENT_SUMMARY:
            return event.get("SUMMARY", "")
        elif field == EVENT_DESCRIPTION:
            return event.get("DESCRIPTION", "")
        elif field == EVENT_STATUS:
            return event["STATUS"]
        elif field == EVENT_LOCATION:
            return event.get("LOCATION", "")
        elif field == EVENT_RECURRENCE:
            return event.get("RRULE")
        elif field == EVENT_START:
            if "DTSTART" in event:
                return event["DTSTART"].dt
            else:
                return None
        elif field == EVENT_END:
            if "DTEND" in event:
                return event["DTEND"].dt
            else:
                return None
        elif field == EVENT_UPDATED:
            if "DTSTAMP" in event:
                return event["DTSTAMP"].dt
            else:
                return None
        else:
            raise Exception("Unhandled event field: %s" % field)
    else:
        if field == EVENT_ID:
            return event["id"]
        elif field == EVENT_ICALUID:
            return event.get("iCalUID")
        elif field == EVENT_SUMMARY:
            return event.get("summary", "")
        elif field == EVENT_DESCRIPTION:
            return event.get("description", "")
        elif field == EVENT_STATUS:
            return event["status"]
        elif field == EVENT_LOCATION:
            return event.get("location", "")
        elif field == EVENT_RECURRENCE:
            return event.get("recurrence")
        elif field == EVENT_START:
            if "start" in event:
                d = event["start"]
                if "dateTime" in d:
                    return datetime.fromisoformat(d["dateTime"])
                else:
                    return datetime.strptime(d["date"], "%Y-%m-%d").date()
            else:
                return None
        elif field == EVENT_END:
            if "end" in event:
                d = event["end"]
                if "dateTime" in d:
                    return datetime.fromisoformat(d["dateTime"])
                else:
                    return datetime.strptime(d["date"], "%Y-%m-%d").date()
            else:
                return None
        elif field == EVENT_UPDATED:
            if "updated" in event:
                return datetime.fromisoformat(event["updated"].replace("Z", "+00:00"))
            else:
                return None
        else:
            raise Exception("Unhandled event field: %s" % field)


def is_same_event(outlook, google) -> bool:
    """
    Compares the two events whether they are the same.

    :param outlook: the Outlook event
    :param google: the Google Calendar event
    :return: True if they represent the same event
    :rtype: bool
    """
    oid = event_field(outlook, EVENT_ID)
    gid = google["iCalUID"] if ("iCalUID" in google) else ""
    return oid == gid


def has_event_changed(outlook, google) -> bool:
    """
    Checks whether at least one field differ sbetween the corresponding Outlook/Google events.

    :param outlook: the Outlook event
    :param google: the Google Calendar event
    :return: True if at least one field changed
    :rtype: bool
    """
    result = False

    for field in EVENT_COMPARISON_FIELDS:
        ovalue = event_field(outlook, field)
        gvalue = event_field(google, field)
        if field == EVENT_UPDATED:
            # only flag as changed if Outlook is newer
            if gvalue < ovalue:
                continue
        if ovalue != gvalue:
            logger().info("event changed: %s" % event_field(outlook, EVENT_ID))
            logger().info("- field/outlook/google: %s/%s/%s" % (field, ovalue, gvalue))
            result = True
            break

    return result


def date_range(events: List[Any]) -> Tuple[Optional[date], Optional[date]]:
    """
    Determines the date range of the events and returns the start/end date objects.

    :param events: the events to process
    :type events: list
    :return: the tuple of start/end date objects; can be None if no start/end dates found
    :rtype: tuple
    """
    start = None
    end = None

    for event in events:
        ds = event_field(event, EVENT_START)
        if isinstance(ds, datetime):
            ds = ds.date()
        de = event_field(event, EVENT_END)
        if isinstance(de, datetime):
            de = de.date()
        if (ds is None) or (de is None):
            continue
        if (start is None) or (start > ds):
            start = ds
        if (end is None) or (end < de):
            end = de

    return start, end
