from akorn.scrapers.base import BaseScraper

from datetime import datetime
import time

class Scraper(BaseScraper):
    # List of domains that scraper is for
    domains = ['oxfordjournals.org', 'cercor.oxfordjournals.org']
    # Relative name of config file
    config = 'oup.json'

    def clean(self, data):
        data = super(Scraper, self).clean(data)

        # Add a date timestamp based on date_journal
        date_str = data.get('date_published')
        if date_str:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            data['date_published'] = time.mktime(date_obj.timetuple())
        return data
