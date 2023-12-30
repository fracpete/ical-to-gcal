import logging
import os

import icalendar
import requests


_logger = None


def logger() -> logging.Logger:
    """
    Return the logger to use.

    :return: the logger
    :rtype: logging.Logger
    """
    global _logger
    if _logger is None:
        _logger = logging.getLogger("otg.api.outlook")
    return _logger


def load_calendar_from_url(url: str) -> icalendar.Calendar:
    """
    Loads a calendar from a URL.

    :param url: the URL to load the calendar from
    :type url: str
    :return: the calendar
    :rtype: icalendar.Calendar
    """
    logger().info("Downloading calendar: %s" % url)
    r = requests.get(url)
    if r.status_code == 200:
        result = icalendar.Calendar.from_ical(r.text)
        return result
    else:
        raise Exception("Failed to retrieve Outlook calendar '%s', status code: %d" % (url, r.status_code))


def load_calendar_from_path(path: str) -> icalendar.Calendar:
    """
    Loads a calendar from a file.

    :param path: the calendar file to load
    :type path: str
    :return: the calendar
    :rtype: icalendar.Calendar
    """
    logger().info("Loading calendar: %s" % path)
    if os.path.exists(path) and os.path.isfile(path):
        with open(path) as fp:
            result = icalendar.Calendar.from_ical(fp.read())
            return result
    else:
        raise IOError("Calendar file does not exist: %s" % path)


def load_calendar(path_or_url: str) -> icalendar.Calendar:
    """
    Loads the shared Outlook calendar by its public .ics path or URL.

    :param path_or_url: the path or URL of the calendar to load
    :type path_or_url: str
    :return: the calendar
    :rtype: icalendar.Calendar
    """
    if path_or_url.startswith("http:") or path_or_url.startswith("https:"):
        return load_calendar_from_url(path_or_url)
    else:
        return load_calendar_from_path(path_or_url)
