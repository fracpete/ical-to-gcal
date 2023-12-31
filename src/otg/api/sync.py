import logging

from typing import List, Dict

from otg.api.events import EVENT_ID, EVENT_SUMMARY, EVENT_DESCRIPTION, EVENT_LOCATION, EVENT_RECURRENCE, EVENT_STATUS
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


def compare(outlook_events: List, google_events: List) -> Dict[str, List]:
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
                    result[ACTION_UPDATE].append(oevent)
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


def sync(service, actions: Dict[str, List]):
    """
    Performs the sync.

    :param service: the Google Calendar service instance to use
    :param actions: the dictionary with the add/delete/update event lists
    :type actions: dict
    """
    for action in actions:
        if action == ACTION_ADD:
            # TODO
            pass
        elif action == ACTION_UPDATE:
            # TODO
            pass
        elif action == ACTION_DELETE:
            # TODO
            pass
