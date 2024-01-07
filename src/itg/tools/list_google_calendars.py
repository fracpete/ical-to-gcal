import argparse
import traceback

from wai.logging import init_logging, add_logging_level
from itg.api.google import init_service


PROG = "itg-list-gcals"


def list_calendars(credentials: str):
    """
    Lists the calendars.

    :param credentials: the path to the credentials JSON file
    :type credentials: str
    """
    service = init_service(credentials)
    list_result = (
        service.calendarList()
        .list(
            showDeleted=False,
            showHidden=False,
        )
        .execute()
    )
    cals = list_result.get("items", [])

    if not cals:
        print("No calendars found.")
        return

    for i, cal in enumerate(cals):
        index = "%d." % (i+1)
        print(index, cal['summary'])
        print(" " * len(index), cal['id'])
        print()


def main():
    parser = argparse.ArgumentParser(
        description='Lists available Google calendars and their IDs.',
        prog=PROG,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-L', '--google_credentials', metavar="FILE", type=str, help='Path to the Google OAuth credentials JSON file', required=True)
    add_logging_level(parser)
    parsed = parser.parse_args()

    init_logging(default_level=parsed.logging_level)
    list_calendars(parsed.google_credentials)


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
