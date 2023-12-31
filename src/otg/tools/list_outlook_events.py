import argparse
import traceback

from wai.logging import init_logging, add_logging_level
from otg.api.outlook import load_calendar, filter_events
from otg.api.events import event_field, EVENT_ID, EVENT_SUMMARY, EVENT_START, EVENT_END, EVENT_RECURRENCE


PROG = "otg-list-oevents"


def list_events(calendar: str, regexp_id: str = None, regexp_summary: str = None):
    """
    Lists the events from the Outlook calendar.

    :param calendar: the path or URL of the Outlook calendar to list
    :type calendar: str
    :param regexp_id: the regular expression that the event IDs must match, ignored if None
    :type regexp_id: str
    :param regexp_summary: the regular expression that the event summaries must match, ignored if None
    :type regexp_summary: str
    """
    cal = load_calendar(calendar)
    events = filter_events(cal, regexp_id=regexp_id, regexp_summary=regexp_summary)
    for event in events:
        print(event_field(event, EVENT_ID))
        if event_field(event, EVENT_SUMMARY) is not None:
            print("   summary:", event_field(event, EVENT_SUMMARY))
        if event_field(event, EVENT_START) is not None:
            print("   start:", event_field(event, EVENT_START))
        if event_field(event, EVENT_END) is not None:
            print("   end:", event_field(event, EVENT_END))
        if event_field(event, EVENT_RECURRENCE) is not None:
            print("   recurrence rule: ", event_field(event, EVENT_RECURRENCE))
        print()


def main():
    parser = argparse.ArgumentParser(
        description='Lists the events in the Outlook Calendar.',
        prog=PROG,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--outlook_calendar', metavar="ID", type=str, help='The path or URL of the Outlook calendar', required=True)
    parser.add_argument('-i', '--outlook_id', metavar="REGEXP", type=str, help='The regular expression that the event IDs must match.', required=False, default=None)
    parser.add_argument('-s', '--outlook_summary', metavar="REGEXP", type=str, help='The regular expression that the event summary must match.', required=False, default=None)
    add_logging_level(parser)
    parsed = parser.parse_args()

    init_logging(default_level=parsed.logging_level)
    list_events(parsed.outlook_calendar, regexp_id=parsed.outlook_id, regexp_summary=parsed.outlook_summary)


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
