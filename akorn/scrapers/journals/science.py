from akorn.scrapers.base import BaseScraper

class Scraper(BaseScraper):
    # List of feeds that scraper is for
    feeds = [
            'http://www.sciencemag.org/rss/current.xml',
        ]
    # List of domains that scraper is for
    domains = [
        'www.sciencemag.org',
        ]
    # Relative name of config file
    config = 'science.json'
