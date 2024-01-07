import argparse
import traceback

from wai.logging import init_logging, add_logging_level
from itg.api.outlook import load_calendar, filter_events
from itg.api.events import event_field, date_range, EVENT_ID, EVENT_SUMMARY, EVENT_START, EVENT_END, EVENT_RECURRENCE, EVENT_STATUS


PROG = "itg-list-oevents"


def list_events(calendar: str, regexp_id: str = None, regexp_summary: str = None, output_file: str = None):
    """
    Lists the events from the iCal/Outlook calendar.

    :param calendar: the path or URL of the iCal/Outlook calendar to list
    :type calendar: str
    :param regexp_id: the regular expression that the event IDs must match, ignored if None
    :type regexp_id: str
    :param regexp_summary: the regular expression that the event summaries must match, ignored if None
    :type regexp_summary: str
    :param output_file: the file to save the iCal/Outlook calendar to, ignored if None
    :type output_file: str
    """
    cal = load_calendar(calendar, output_file=output_file)
    events = filter_events(cal, regexp_id=regexp_id, regexp_summary=regexp_summary)
    start, end = date_range(events)
    print("Date range:", start, "-", end)
    print()
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
        if event_field(event, EVENT_STATUS) is not None:
            print("   status:", event_field(event, EVENT_STATUS))
        print()


def main():
    parser = argparse.ArgumentParser(
        description='Lists the events in the iCal/Outlook Calendar.',
        prog=PROG,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--ical_calendar', metavar="ID", type=str, help='The path or URL of the iCal/Outlook calendar', required=True)
    parser.add_argument('-i', '--ical_id', metavar="REGEXP", type=str, help='The regular expression that the event IDs must match.', required=False, default=None)
    parser.add_argument('-s', '--ical_summary', metavar="REGEXP", type=str, help='The regular expression that the event summary must match.', required=False, default=None)
    parser.add_argument('--ical_output', metavar="FILE", type=str, help='The file to save the iCal/Outlook calendar data to.', required=False, default=None)
    add_logging_level(parser)
    parsed = parser.parse_args()

    init_logging(default_level=parsed.logging_level)
    list_events(parsed.ical_calendar, regexp_id=parsed.ical_id, regexp_summary=parsed.ical_summary,
                output_file=parsed.ical_output)


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
