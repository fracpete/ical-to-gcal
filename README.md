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
  -L FILE, --credentials FILE
                        Path to the Google OAuth credentials JSON file
                        (default: None)
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
```

### List Google calendar events

```
usage: otg-list-gevents [-h] -L FILE -g ID [--google_id REGEXP]
                        [--google_summary REGEXP]
                        [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Lists the events in the Outlook Calendar.

optional arguments:
  -h, --help            show this help message and exit
  -L FILE, --credentials FILE
                        Path to the Google OAuth credentials JSON file
                        (default: None)
  -g ID, --google_calendar ID
                        The path or URL of the Outlook calendar (default:
                        None)
  --google_id REGEXP    The regular expression that the event IDs must match.
                        (default: None)
  --google_summary REGEXP
                        The regular expression that the event summary must
                        match. (default: None)
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
```


### List Outlook calendar events

```
usage: otg-list-oevents [-h] -o ID [--outlook_id REGEXP]
                        [--outlook_summary REGEXP]
                        [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Lists the events in the Outlook Calendar.

optional arguments:
  -h, --help            show this help message and exit
  -o ID, --outlook_calendar ID
                        The path or URL of the Outlook calendar (default:
                        None)
  --outlook_id REGEXP   The regular expression that the event IDs must match.
                        (default: None)
  --outlook_summary REGEXP
                        The regular expression that the event summary must
                        match. (default: None)
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        The logging level to use. (default: WARN)
```

