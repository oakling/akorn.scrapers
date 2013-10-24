import requests
from xml.etree import ElementTree

from akorn.scrapers.base import BaseScraper

class Scraper(BaseScraper):
    # List of feeds that scraper is for
    # TODO Lots more here: http://www.oxfordjournals.org/subject/mathematics/
    feeds = [
        'http://cercor.oxfordjournals.org/rss/ahead.xml',
        'http://abbs.oxfordjournals.org/rss/ahead.xml',
        'http://bioinformatics.oxfordjournals.org/rss/ahead.xml',
        'http://biomet.oxfordjournals.org/rss/ahead.xml',
        'http://biostatistics.oxfordjournals.org/rss/ahead.xml'
        ]
    # List of domains that scraper is for
    domains = [
        'cercor.oxfordjournals.org',
        'abbs.oxfordjournals.org',
        'bioinformatics.oxfordjournals.org',
        'biostatistics.oxfordjournals.org',
        ]
    # Relative name of config file
    config = 'oup.json'

    def getUrlList(self):
        """Get the list of urls from:
        http://www.oxfordjournals.org/help/oxfordjournals.opml.xml"""
        xml_list = requests.urlopen('http://www.oxfordjournals.org/help/oxfordjournals.opml.xml')
        xml_parse = ElementTree.parse(xml_list)

if name == __main__:
    import pdb;pdb.set_trace()
    #return Scraper.getUrlList()
