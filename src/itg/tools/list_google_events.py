import argparse
import traceback

from wai.logging import init_logging, add_logging_level
from itg.api.google import init_service, filter_events
from itg.api.events import event_field, date_range, EVENT_ID, EVENT_SUMMARY, EVENT_START, EVENT_END, EVENT_RECURRENCE, EVENT_ICALUID


PROG = "itg-list-gevents"


def list_events(credentials: str, calendar: str, regexp_id: str = None, regexp_summary: str = None):
    """
    Lists the events from the Google calendar.

    :param credentials: the credentials JSON file to use
    :type credentials: str
    :param calendar: the calendar ID
    :type calendar: str
    :param regexp_id: the regular expression that the event IDs must match, ignored if None
    :type regexp_id: str
    :param regexp_summary: the regular expression that the event summaries must match, ignored if None
    :type regexp_summary: str
    """
    service = init_service(credentials)
    events = filter_events(service, calendar, regexp_id=regexp_id, regexp_summary=regexp_summary)
    start, end = date_range(events)
    print("Date range:", start, "-", end)
    print()
    for event in events:
        print(event_field(event, EVENT_ID))
        print("   summary:", event_field(event, EVENT_SUMMARY))
        if event_field(event, EVENT_START) is not None:
            print("   start:", event_field(event, EVENT_START))
        if event_field(event, EVENT_END) is not None:
            print("   end:", event_field(event, EVENT_END))
        if event_field(event, EVENT_RECURRENCE) is not None:
            print("   recurrence rule:", event_field(event, EVENT_RECURRENCE))
        if event_field(event, EVENT_ICALUID) is not None:
            print("   iCalUID:", event_field(event, EVENT_ICALUID))
        print()
        if "nextPageToken" in event:
            print("...not all events listed")


def main():
    parser = argparse.ArgumentParser(
        description='Lists the events in the Outlook Calendar.',
        prog=PROG,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-L', '--google_credentials', metavar="FILE", type=str, help='Path to the Google OAuth credentials JSON file', required=True)
    parser.add_argument('-C', '--google_calendar', metavar="ID", type=str, help='The path or URL of the Outlook calendar', required=True)
    parser.add_argument('-I', '--google_id', metavar="REGEXP", type=str, help='The regular expression that the event IDs must match.', required=False, default=None)
    parser.add_argument('-S', '--google_summary', metavar="REGEXP", type=str, help='The regular expression that the event summary must match.', required=False, default=None)
    add_logging_level(parser)
    parsed = parser.parse_args()

    init_logging(default_level=parsed.logging_level)
    list_events(parsed.google_credentials, parsed.google_calendar, regexp_id=parsed.google_id, regexp_summary=parsed.google_summary)


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
