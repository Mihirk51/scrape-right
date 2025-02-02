BASE_URL = 'https://www.vlr.gg/'
EVENTS_BASE_URL = BASE_URL + 'events/'

REGIONS = {
    "na": "north-america",
    "eu": "europe",
    "br": "brazil",
    "ap": "asia-pacific",
    "kr": "korea",
    "jp": "japan",
    "sa": "latin-america",
    "oce": "oceania",
    "mn": "mena",
    "gc": "game-changers",
    "col": "collegiate",
}

REGION_MAPPING_LINKS = {
    key: f"{EVENTS_BASE_URL}{value}"
    for key, value in REGIONS.items()
}

CHROMEDRIVER_PATH = 'chromedriver.exe'
SLEEP_TIME = 1  # seconds for waiting after page loads