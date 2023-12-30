# outlook-to-gcal
Syncing Outlook Calendar with Google Calendar

## Requirements

* Outlook
  
  * Publish the calendar that you want to sync with Google Calendar

* Google

  * Create app and follow [these instructions](https://developers.google.com/calendar/api/quickstart/python)


## Installation

```bash
pip install git+https://github.com/fracpete/outlook-to-gcal.git
```

## Tools

### List Google Calendars

```
usage: otg-list-gcals [-h] -L CREDENTIALS
                      [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Lists available Google calendars and their IDs.

optional arguments:
  -h, --help            show this help message and exit
  -L CREDENTIALS, --credentials CREDENTIALS
                        Path to the Google OAuth credentials JSON file
                        (default: None)
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
```

### List Outlook calendar events

```
usage: otg-list-oevents [-h] -c CALENDAR [-i REGEXP_ID] [-s REGEXP_SUMMARY]
                        [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Lists the events in the Outlook Calendar.

optional arguments:
  -h, --help            show this help message and exit
  -c CALENDAR, --calendar CALENDAR
                        The path or URL of the Outlook calendar (default:
                        None)
  -i REGEXP_ID, --regexp_id REGEXP_ID
                        The regular expression that the event IDs must match.
                        (default: None)
  -s REGEXP_SUMMARY, --regexp_summary REGEXP_SUMMARY
                        The regular expression that the event summary must
                        match. (default: None)
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
```

