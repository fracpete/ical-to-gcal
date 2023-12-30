import argparse
import re
import traceback

from wai.logging import init_logging, add_logging_level
from otg.api.outlook import load_calendar


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
    for event in cal.walk('VEVENT'):
        id = event.get("UID")
        if regexp_id is not None:
            match = re.match(regexp_id, id)
            if not match:
                continue
        summary = event.get("SUMMARY")
        if regexp_summary is not None:
            match = re.match(regexp_summary, summary)
            if not match:
                continue
        print(id)
        print("   summary: ", summary)
        print()


def main():
    parser = argparse.ArgumentParser(
        description='Lists the events in the Outlook Calendar.',
        prog=PROG,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--calendar', type=str, help='The path or URL of the Outlook calendar', required=True)
    parser.add_argument('-i', '--regexp_id', type=str, help='The regular expression that the event IDs must match.', required=False, default=None)
    parser.add_argument('-s', '--regexp_summary', type=str, help='The regular expression that the event summary must match.', required=False, default=None)
    add_logging_level(parser)
    parsed = parser.parse_args()

    init_logging(default_level=parsed.logging_level)
    list_events(parsed.calendar, regexp_id=parsed.regexp_id, regexp_summary=parsed.regexp_summary)


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