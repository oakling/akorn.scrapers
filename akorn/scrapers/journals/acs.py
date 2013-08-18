from akorn.scrapers.base import BaseScraper

from dateutil import parser
import time

class Scraper(BaseScraper):
    # List of feeds that scraper is for
    feeds = ['http://feeds.feedburner.com/acs/jacsat']
    # Where to find the URL in each feed item
    feed_tag = 'feedburner_origlink'
    # List of domains that scraper is for
    domains = ['pubs.acs.org']
    # Relative name of config file
    config = 'acs.json'
