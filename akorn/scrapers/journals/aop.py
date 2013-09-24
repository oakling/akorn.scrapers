from akorn.scrapers.base import BaseScraper

class Scraper(BaseScraper):
    # List of feeds that scraper is for
    feeds = [
        'http://metadata.osa.org/rss/infobase/aop_feed.xml'
        ]
    # List of domains that scraper is for
    domains = [
        'www.opticsinfobase.org'
        ]
    # Relative name of config file
    config = 'aop.json'
