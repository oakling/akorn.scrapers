from akorn.scrapers.base import BaseScraper

import time, datetime
import re

months = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12}

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

    def clean(self, data):
        data = super(Scraper, self).clean(data)

        date_str = data['date_published']
        
        date_received = re.findall('Received\s+([0-9]+)\s+([A-Za-z]+)\s+([0-9]+)', date_str)
        date_revised = re.findall('revised\s+([0-9]+)\s+([A-Za-z]+)\s+([0-9]+)', date_str)
        date_published = re.findall('published\s+([0-9]+)\s+([A-Za-z]+)\s+([0-9]+)', date_str)

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
