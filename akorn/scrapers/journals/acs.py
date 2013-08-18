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

    def clean(self, data):
        data = super(Scraper, self).clean(data)
        # Add a date timestamp based on date_published
        date_str = data.get('date_published')
        if date_str:
            # Do fuzzy date parsing
            date_obj = parser.parse(date_str)
            # Convert date to timestamp
            data['date_published'] = time.mktime(date_obj.timetuple())
        return data
