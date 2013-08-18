from akorn.scrapers.base import BaseScraper

from dateutil import parser
import time

class Scraper(BaseScraper):
    # List of feeds that scraper is for
    feeds = [
                (
                    "http://feeds.feedburner.com/acs/jacsat",
                    "feedburner_origlink",
                    {"minute":1, "hour": "15"},
                )
            ]
    # List of domains that scraper is for
    domains = ['pubs.acs.org']
    # Relative name of config file
    config = 'acs.json'
