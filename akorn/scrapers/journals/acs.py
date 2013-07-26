from akorn.scrapers.base import BaseScraper

import dateutil
import time

class Scraper(BaseScraper):
    # List of domains that scraper is for
    domains = ['pubs.acs.org']
    # Relative name of config file
    config = 'acs.xml'

    def clean(self, data):
        data = super(Scraper, self).clean(data)
        # Add a date timestamp based on date_published
        date_str = data.get('date_published')
        if date_str:
            # Do fuzzy date parsing
            date_obj = dateutil.parser.parse(date_str)
            # Convert date to timestamp
            data['date_published'] = time.mktime(date_obj.timetuple())
        return data
