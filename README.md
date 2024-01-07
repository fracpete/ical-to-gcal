# ical-to-gcal
Syncing iCal calendars like Outlook (from Office 365) with Google Calendar.


## Documentation

* [icalendar library](https://icalendar.readthedocs.io/en/latest/)
* [Google Calendar API](https://developers.google.com/resources/api-libraries/documentation/calendar/v3/python/latest/) ([quickstart Python](https://developers.google.com/calendar/api/quickstart/python))


## Requirements

* iCal

  * Outlook: publish the calendar that you want to sync with Google Calendar
  * Other: either obtain public URL for `.ics` calendar or download calendar in iCal format

* Google

  * Enable Calendar API and create app as per [these instructions](https://developers.google.com/calendar/api/quickstart/python)
  * Download the credentials as `credentials.json` and store them in a safe location


## Installation

```bash
pip install git+https://github.com/fracpete/outlook-to-gcal.git
```


## How to sync

Setup Outlook:

* fulfill above requirements
* install library as per above
* publish Outlook Calendar and determine its URL (Settings -> Calendar -> Share Calendars -> Publish a Calendar -> `OUTLOOK_ICS_URL`)
* create new Google Calendar (makes it easier to remove when stuffed up)
* determine ID of Google Calendar using `itg-list-gcals` tool below (`GCAL_ID`)

The following will perform a sync every 15min:

```bash
itg-sync-cals \
  -l INFO \
  -c OUTLOOK_ICS_URL \
  -i "[^@]+ " \
  -L /safe/location/credentials.json \
  -C GCAL_ID \
  -p 900
```

Notes:

* `-l INFO` - outputs some logging information
* `-i "[^@]+"` - omits Outlook Calendar entries that have come from Google (`LONG_ID@gmail.com`)
* Treat the Google Calendar as read-only and only add/update/delete calendar entries in the Outlook one,
  otherwise you will end up with errors (e.g., `duplicate entry`)


## Tools

### List Google calendars

```
usage: itg-list-gcals [-h] -L FILE [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Lists available Google calendars and their IDs.

optional arguments:
  -h, --help            show this help message and exit
  -L FILE, --google_credentials FILE
                        Path to the Google OAuth credentials JSON file
                        (default: None)
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
```


### List Google calendar events

```
usage: itg-list-gevents [-h] -L FILE -C ID [-I REGEXP] [-S REGEXP]
                        [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Lists the events in the Outlook Calendar.

optional arguments:
  -h, --help            show this help message and exit
  -L FILE, --google_credentials FILE
                        Path to the Google OAuth credentials JSON file
                        (default: None)
  -C ID, --google_calendar ID
                        The path or URL of the Outlook calendar (default:
                        None)
  -I REGEXP, --google_id REGEXP
                        The regular expression that the event IDs must match.
                        (default: None)
  -S REGEXP, --google_summary REGEXP
                        The regular expression that the event summary must
                        match. (default: None)
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
```


### List Outlook calendar events

```
usage: itg-list-oevents [-h] -c ID [-i REGEXP] [-s REGEXP]
                        [--ical_output FILE]
                        [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Lists the events in the iCal/Outlook Calendar.

optional arguments:
  -h, --help            show this help message and exit
  -c ID, --ical_calendar ID
                        The path or URL of the iCal/Outlook calendar (default:
                        None)
  -i REGEXP, --ical_id REGEXP
                        The regular expression that the event IDs must match.
                        (default: None)
  -s REGEXP, --ical_summary REGEXP
                        The regular expression that the event summary must
                        match. (default: None)
  --ical_output FILE    The file to save the iCal/Outlook calendar data to.
                        (default: None)
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
```


### Compare calendars

```
usage: itg-compare-cals [-h] -c ID [-i REGEXP] [-s REGEXP] -L FILE -C ID
                        [-I REGEXP] [-S REGEXP]
                        [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Compares the iCal/Outlook and Google Calendar and outputs the proprosed
actions.

optional arguments:
  -h, --help            show this help message and exit
  -c ID, --ical_calendar ID
                        The path or URL of the iCal/Outlook calendar (default:
                        None)
  -i REGEXP, --ical_id REGEXP
                        The regular expression that the event IDs must match.
                        (default: None)
  -s REGEXP, --ical_summary REGEXP
                        The regular expression that the event summary must
                        match. (default: None)
  -L FILE, --google_credentials FILE
                        Path to the Google OAuth credentials JSON file
                        (default: None)
  -C ID, --google_calendar ID
                        The ID of the Google calendar (default: None)
  -I REGEXP, --google_id REGEXP
                        The regular expression that the event IDs must match.
                        (default: None)
  -S REGEXP, --google_summary REGEXP
                        The regular expression that the event summary must
                        match. (default: None)
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
```


### Sync calendars

```
usage: itg-sync-cals [-h] -c ID [-i REGEXP] [-s REGEXP] [--ical_output FILE]
                     -L FILE -C ID [-I REGEXP] [-S REGEXP] [-n] [-p SEC]
                     [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Syncs the iCal/Outlook calendar with the Google one.

optional arguments:
  -h, --help            show this help message and exit
  -c ID, --ical_calendar ID
                        The path or URL of the iCal/Outlook calendar (default:
                        None)
  -i REGEXP, --ical_id REGEXP
                        The regular expression that the event IDs must match.
                        (default: None)
  -s REGEXP, --ical_summary REGEXP
                        The regular expression that the event summary must
                        match. (default: None)
  --ical_output FILE    The file to save the iCal/Outlook calendar data to.
                        (default: None)
  -L FILE, --google_credentials FILE
                        Path to the Google OAuth credentials JSON file
                        (default: None)
  -C ID, --google_calendar ID
                        The path or URL of the Outlook calendar (default:
                        None)
  -I REGEXP, --google_id REGEXP
                        The regular expression that the event IDs must match.
                        (default: None)
  -S REGEXP, --google_summary REGEXP
                        The regular expression that the event summary must
                        match. (default: None)
  -n, --dry_run         Whether to perform a dry-run instead, not changing
                        Google calendar at all. (default: False)
  -p SEC, --poll_interval SEC
                        The interval to poll the Outlook calendar in seconds.
                        (default: None)
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
```
