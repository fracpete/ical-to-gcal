import argparse
import logging
import traceback

from time import sleep

from wai.logging import init_logging, add_logging_level
from otg.api.outlook import load_calendar
from otg.api.outlook import filter_events as ofilter_events
from otg.api.google import init_service
from otg.api.google import filter_events as gfilter_events
from otg.api.sync import compare, sync


PROG = "otg-sync-cals"


_logger = None


def logger() -> logging.Logger:
    """
    Return the logger to use.

    :return: the logger
    :rtype: logging.Logger
    """
    global _logger
    if _logger is None:
        _logger = logging.getLogger(PROG)
    return _logger


def sync_events(outlook_calendar: str, google_credentials: str, google_calendar: str,
                outlook_id: str = None, outlook_summary: str = None, outlook_output: str = None,
                google_id: str = None, google_summary: str = None,
                dry_run: bool = False, poll_interval: int = None):
    """
    Syncs the events from the Outlook calendar with the Google one.

    :param outlook_calendar: the path or URL of the Outlook calendar to list
    :type outlook_calendar: str
    :param outlook_id: the regular expression that the event IDs must match, ignored if None
    :type outlook_id: str
    :param outlook_summary: the regular expression that the event summaries must match, ignored if None
    :type outlook_summary: str
    :param outlook_output: the file to save the outlook calendar to, ignored if None
    :type outlook_output: str
    :param google_credentials: the credentials JSON file to use
    :type google_credentials: str
    :param google_calendar: the calendar ID
    :type google_calendar: str
    :param google_id: the regular expression that the event IDs must match, ignored if None
    :type google_id: str
    :param google_summary: the regular expression that the event summaries must match, ignored if None
    :type google_summary: str
    :param dry_run: whether to perform a dry-run only and not change the Google Calendar at all
    :type dry_run: bool
    :param poll_interval: the interval in seconds to poll the Outlook calendar, only once if None
    :type poll_interval: int
    """
    while True:
        # outlook
        outlook_cal = load_calendar(outlook_calendar, output_file=outlook_output)
        outlook_events = ofilter_events(outlook_cal, regexp_id=outlook_id, regexp_summary=outlook_summary)

        # google
        google_service = init_service(google_credentials)
        google_events = gfilter_events(google_service, google_calendar, regexp_id=google_id, regexp_summary=google_summary)

        comparison = compare(outlook_events, google_events)
        errors = sync(google_service, google_calendar, comparison, dry_run=dry_run)
        num_errors = sum([len(errors[x]) for x in errors])
        if num_errors > 0:
            logger().warning("%d errors occurred!")

        if poll_interval is None:
            break
        else:
            logger().info("Waiting %d seconds before next poll..." % poll_interval)
            sleep(poll_interval)


def main():
    parser = argparse.ArgumentParser(
        description='Syncs the Outlook calendar with the Google one.',
        prog=PROG,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--outlook_calendar', metavar="ID", type=str, help='The path or URL of the Outlook calendar', required=True)
    parser.add_argument('-i', '--outlook_id', metavar="REGEXP", type=str, help='The regular expression that the event IDs must match.', required=False, default=None)
    parser.add_argument('-s', '--outlook_summary', metavar="REGEXP", type=str, help='The regular expression that the event summary must match.', required=False, default=None)
    parser.add_argument('--outlook_output', metavar="FILE", type=str, help='The file to save the Outlook calendar data to.', required=False, default=None)
    parser.add_argument('-L', '--google_credentials', metavar="FILE", type=str, help='Path to the Google OAuth credentials JSON file', required=True)
    parser.add_argument('-C', '--google_calendar', metavar="ID", type=str, help='The path or URL of the Outlook calendar', required=True)
    parser.add_argument('-I', '--google_id', metavar="REGEXP", type=str, help='The regular expression that the event IDs must match.', required=False, default=None)
    parser.add_argument('-S', '--google_summary', metavar="REGEXP", type=str, help='The regular expression that the event summary must match.', required=False, default=None)
    parser.add_argument('-n', '--dry_run', action="store_true", help='Whether to perform a dry-run instead, not changing Google calendar at all.')
    parser.add_argument('-p', '--poll_interval', metavar="SEC", type=int, help='The interval to poll the Outlook calendar in seconds.', required=False, default=None)
    add_logging_level(parser)
    parsed = parser.parse_args()

    init_logging(default_level=parsed.logging_level)
    sync_events(parsed.outlook_calendar, parsed.google_credentials, parsed.google_calendar,
                outlook_id=parsed.outlook_id, outlook_summary=parsed.outlook_summary,
                outlook_output=parsed.outlook_output,
                google_id=parsed.google_id, google_summary=parsed.google_summary,
                dry_run=parsed.dry_run, poll_interval=parsed.poll_interval)


def sys_main() -> int:
    """
    Runs the main function using the system cli arguments, and
    returns a system error code.

    :return: 0 for success, 1 for failure.
    """
    try:
        main()
        return 0
    except Exception:
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    main()
