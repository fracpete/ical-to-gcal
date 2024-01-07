import argparse
import traceback

from wai.logging import init_logging, add_logging_level
from itg.api.outlook import load_calendar
from itg.api.outlook import filter_events as ofilter_events
from itg.api.google import init_service
from itg.api.google import filter_events as gfilter_events
from itg.api.sync import compare, ACTIONS


PROG = "itg-compare-cals"


def compare_events(ical_calendar: str, google_credentials: str, google_calendar: str,
                   ical_id: str = None, ical_summary: str = None,
                   google_id: str = None, google_summary: str = None):
    """
    Lists the events from the iCal/Outlook calendar.

    :param ical_calendar: the path or URL of the iCal/Outlook calendar to list
    :type ical_calendar: str
    :param ical_id: the regular expression that the event IDs must match, ignored if None
    :type ical_id: str
    :param ical_summary: the regular expression that the event summaries must match, ignored if None
    :type ical_summary: str
    :param google_credentials: the credentials JSON file to use
    :type google_credentials: str
    :param google_calendar: the calendar ID
    :type google_calendar: str
    :param google_id: the regular expression that the event IDs must match, ignored if None
    :type google_id: str
    :param google_summary: the regular expression that the event summaries must match, ignored if None
    :type google_summary: str
    """
    # outlook
    ical_cal = load_calendar(ical_calendar)
    ical_events = ofilter_events(ical_cal, regexp_id=ical_id, regexp_summary=ical_summary)

    # google
    google_service = init_service(google_credentials)
    google_events = gfilter_events(google_service, google_calendar, regexp_id=google_id, regexp_summary=google_summary)

    comparison = compare(ical_events, google_events)
    for action in ACTIONS:
        if action in comparison:
            events = comparison[action]
            print(action)
            print("=" * len(action))
            for event in events:
                print("   ", event)
            print()


def main():
    parser = argparse.ArgumentParser(
        description='Compares the iCal/Outlook and Google Calendar and outputs the proprosed actions.',
        prog=PROG,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--ical_calendar', metavar="ID", type=str, help='The path or URL of the iCal/Outlook calendar', required=True)
    parser.add_argument('-i', '--ical_id', metavar="REGEXP", type=str, help='The regular expression that the event IDs must match.', required=False, default=None)
    parser.add_argument('-s', '--ical_summary', metavar="REGEXP", type=str, help='The regular expression that the event summary must match.', required=False, default=None)
    parser.add_argument('-L', '--google_credentials', metavar="FILE", type=str, help='Path to the Google OAuth credentials JSON file', required=True)
    parser.add_argument('-C', '--google_calendar', metavar="ID", type=str, help='The ID of the Google calendar', required=True)
    parser.add_argument('-I', '--google_id', metavar="REGEXP", type=str, help='The regular expression that the event IDs must match.', required=False, default=None)
    parser.add_argument('-S', '--google_summary', metavar="REGEXP", type=str, help='The regular expression that the event summary must match.', required=False, default=None)
    add_logging_level(parser)
    parsed = parser.parse_args()

    init_logging(default_level=parsed.logging_level)
    compare_events(parsed.ical_calendar, parsed.google_credentials, parsed.google_calendar,
                   ical_id=parsed.ical_id, ical_summary=parsed.ical_summary,
                   google_id=parsed.google_id, google_summary=parsed.google_summary)


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
