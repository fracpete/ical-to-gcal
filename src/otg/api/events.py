from typing import Optional, Union

import icalendar

EVENT_ID = "id"
EVENT_SUMMARY = "summary"
EVENT_LOCATION = "location"
EVENT_RECURRENCE = "recurrence"
EVENT_STATUS = "status"
EVENT_START = "start"
EVENT_END = "end"

EVENT_FIELDS = [
    EVENT_ID,
    EVENT_SUMMARY,
    EVENT_LOCATION,
    EVENT_RECURRENCE,
    EVENT_STATUS,
    EVENT_START,
    EVENT_END,
]


def event_field(event, field: str) -> Optional[Union[str, object]]:
    """
    Returns the specified event value.

    :param event: the event to get the value fromm
    :param field: the name of the field to retrieve
    :type field: str
    :return: the value, can be None
    """
    if field not in EVENT_FIELDS:
        raise Exception("Unknown event field: %s" % field)

    if isinstance(event, icalendar.Event):
        if field == EVENT_ID:
            return event["UID"]
        elif field == EVENT_SUMMARY:
            if "SUMMARY" in event:
                return event["SUMMARY"]
            else:
                return ""
        elif field == EVENT_STATUS:
            return event["STATUS"]
        elif field == EVENT_LOCATION:
            return event["LOCATION"]
        elif field == EVENT_RECURRENCE:
            if "RRULE" in event:
                return event["RRULE"]
            else:
                return None
        elif field == EVENT_START:
            if "DTSTART" in event:
                return event["DTSTART"]
            else:
                return None
        elif field == EVENT_END:
            if "DTEND" in event:
                return event["DTEND"]
            else:
                return None
        else:
            raise Exception("Unhandled event field: %s" % field)
    else:
        if field == EVENT_ID:
            return event["id"]
        elif field == EVENT_SUMMARY:
            if "summary" in event:
                return event["summary"]
            else:
                return ""
        elif field == EVENT_STATUS:
            return event["status"]
        elif field == EVENT_LOCATION:
            return event["location"]
        elif field == EVENT_RECURRENCE:
            if "recurrence" in event:
                return event["recurrence"]
            else:
                return None
        elif field == EVENT_START:
            if "start" in event:
                return event["start"]
            else:
                return None
        elif field == EVENT_END:
            if "end" in event:
                return event["end"]
            else:
                return None
        else:
            raise Exception("Unhandled event field: %s" % field)
