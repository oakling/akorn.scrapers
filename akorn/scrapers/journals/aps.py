import iso8601
from akorn.scrapers.base import BaseScraper

import time, datetime
import re

months = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12}

def get8601date(s):
  return time.mktime(iso8601.parse_date(s).timetuple())

class Scraper(BaseScraper):
    # List of feeds that scraper is for
    feeds = ["http://feeds.aps.org/rss/recent/prl.xml",
             "http://feeds.aps.org/rss/recent/pra.xml",
             "http://feeds.aps.org/rss/recent/prb.xml",
             "http://feeds.aps.org/rss/recent/prc.xml",
             "http://feeds.aps.org/rss/recent/prd.xml",
             "http://feeds.aps.org/rss/recent/pre.xml",
             "http://feeds.aps.org/rss/recent/prx.xml",
             "http://feeds.aps.org/rss/recent/rmp.xml",
             "http://feeds.aps.org/rss/recent/prstab.xml",
             "http://feeds.aps.org/rss/recent/prstper.xml",]

    should_scrape = False

    # Where to find the URL in each feed item
    feed_tag = ['link']

    # List of domains that scraper is for
    domains = ['pra.aps.org',
               'prb.aps.org',
               'prc.aps.org',
               'prd.aps.org',
               'pre.aps.org',
               'prx.aps.org',
               'prl.aps.org',
               'prst-ab.aps.org',
               'prst-per.aps.org',
               'rmp.aps.org',
               'prola.aps.org',
               'link.aps.org',]

    # Relative name of config file
    config = 'aps.json'

    def scrape_rss(self, item):
        doc = {'publisher': 'American Physical Society',}
        doc['title'] = item['title']
        doc['doi'] = item['prism_doi']
        doc['source_urls'] = [item['link']]
        doc['canonical_url'] = item['link']
        doc['journal'] = item['prism_publicationname']
        doc['date_published'] = get8601date(item['prism_publicationdate'])
        doc['date_updated'] = time.mktime(item['updated_parsed'])
        doc['date_scraped'] = int(time.time())
        doc['author_names'] = [a.replace(' and ', '').strip() for a in item['author'].split(',')]
        return doc

    def clean(self, data):
        print data
        date_str = data['date_published']
       
        print type(date_str), date_str 
        date_received = re.findall('Received\s+([0-9]+)\s+([A-Za-z]+)\s+([0-9]+)', date_str)
        date_revised = re.findall('revised\s+([0-9]+)\s+([A-Za-z]+)\s+([0-9]+)', date_str)
        date_published = re.findall('published\s+([0-9]+)\s+([A-Za-z]+)\s+([0-9]+)', date_str)
        
        data = super(Scraper, self).clean(data)

        def make_datestamp(date_tuple):
          year = int(date_tuple[2])
          month = months[date_tuple[1]]
          day = int(date_tuple[0])
          return time.mktime(datetime.date(year, month, day).timetuple())

        if date_received:
          data['date_received'] = make_datestamp(date_received[0])
        if date_revised:
          data['date_revised'] = make_datestamp(date_revised[0])
        if date_published:
          data['date_published'] = make_datestamp(date_published[0])

        return data
