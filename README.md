# outlook-to-gcal
Syncing Outlook Calendar with Google Calendar

## Requirements

* Outlook
  
  * Publish the calendar that you want to sync with Google Calendar

* Google

  * Enable Calendar API and create app as per [these instructions](https://developers.google.com/calendar/api/quickstart/python)


## Installation

```bash
pip install git+https://github.com/fracpete/outlook-to-gcal.git
```

## Tools

### List Google calendars

```
usage: otg-list-gcals [-h] -L FILE [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

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
usage: otg-list-gevents [-h] -L FILE -C ID [-I REGEXP] [-S REGEXP]
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
usage: otg-list-oevents [-h] -c ID [-i REGEXP] [-s REGEXP]
                        [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Lists the events in the Outlook Calendar.

optional arguments:
  -h, --help            show this help message and exit
  -c ID, --outlook_calendar ID
                        The path or URL of the Outlook calendar (default:
                        None)
  -i REGEXP, --outlook_id REGEXP
                        The regular expression that the event IDs must match.
                        (default: None)
  -s REGEXP, --outlook_summary REGEXP
                        The regular expression that the event summary must
                        match. (default: None)
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
```


### Compare calendars

```
usage: otg-compare-cals [-h] -c ID [-i REGEXP] [-s REGEXP] -L FILE -C ID
                        [-I REGEXP] [-S REGEXP]
                        [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Compares the Outlook and Google Calendar and outputs the proprosed actions.

optional arguments:
  -h, --help            show this help message and exit
  -c ID, --outlook_calendar ID
                        The path or URL of the Outlook calendar (default:
                        None)
  -i REGEXP, --outlook_id REGEXP
                        The regular expression that the event IDs must match.
                        (default: None)
  -s REGEXP, --outlook_summary REGEXP
                        The regular expression that the event summary must
                        match. (default: None)
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


### Sync calendars

```
usage: otg-sync-cals [-h] -c ID [-i REGEXP] [-s REGEXP] -L FILE -C ID
                     [-I REGEXP] [-S REGEXP]
                     [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Compares the Outlook and Google Calendar and outputs the proprosed actions.

optional arguments:
  -h, --help            show this help message and exit
  -c ID, --outlook_calendar ID
                        The path or URL of the Outlook calendar (default:
                        None)
  -i REGEXP, --outlook_id REGEXP
                        The regular expression that the event IDs must match.
                        (default: None)
  -s REGEXP, --outlook_summary REGEXP
                        The regular expression that the event summary must
                        match. (default: None)
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
