from setuptools import setup


def _read(f):
    """
    Reads in the content of the file.
    :param f: the file to read
    :type f: str
    :return: the content
    :rtype: str
    """
    return open(f, 'rb').read()


setup(
    name="ical_to_gcal",
    description="Simple command-line tool for syncing an Outlook Calendar with Google Calendar.",
    long_description=(
        _read('DESCRIPTION.rst') + b'\n' +
        _read('CHANGES.rst')).decode('utf-8'),
    url="https://github.com/fracpete/outlook-to-gcal",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Office/Business :: News/Diary',
        'Programming Language :: Python :: 3',
    ],
    license='Apache 2.0',
    package_dir={
        '': 'src'
    },
    packages=[
        "otg",
    ],
    version="0.0.1",
    author='Peter "fracpete" Reutemann',
    author_email='fracpete@gmail.com',
    install_requires=[
        "wai.logging",
        "requests",
        "icalendar",
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
    ],
    entry_points={
        "console_scripts": [
            "itg-list-gcals=itg.tools.list_google_calendars:sys_main",
            "itg-list-gevents=itg.tools.list_google_events:sys_main",
            "itg-list-oevents=itg.tools.list_outlook_events:sys_main",
            "itg-compare-cals=itg.tools.compare_calendars:sys_main",
            "itg-sync-cals=itg.tools.sync_calendars:sys_main",
        ]
    }
)
