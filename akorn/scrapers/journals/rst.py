from akorn.scrapers.base import BaseScraper

class Scraper(BaseScraper):
    # List of feeds that scraper is for
    feeds = [
        'http://rsta.royalsocietypublishing.org/rss/Articles.xml',
        'http://rstb.royalsocietypublishing.org/rss/Articles.xml'
        ]

    # List of domains that scraper is for
    domains = [
        'rsta.royalsocietypublishing.org',
        'rstb.royalsocietypublishing.org']

    # Relative name of config file
    config = 'rst.json'

    def clean(self, data):
      data = super(Scraper, self).clean(data)

      data['journal'] = data['journal'].replace('\t', '').replace('\n', ' ')

      return data
