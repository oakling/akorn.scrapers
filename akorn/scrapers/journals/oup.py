from akorn.scrapers.base import BaseScraper

from datetime import datetime
import time

class Scraper(BaseScraper):
    # List of domains that scraper is for
    domains = ['oxfordjournals.org', 'cercor.oxfordjournals.org']
    # Relative name of config file
    config = 'oup.xml'

    def clean(self, data):
        data = super(Scraper, self).clean(data)

        # Add a date timestamp based on date_journal
	date_journal_str = data.get('date_journal')
        if date_journal_str:
            date_journal = datetime.strptime(date_journal_str, '%Y-%m-%d')
            data['date'] = time.mktime(date_journal.timetuple())
        return data
