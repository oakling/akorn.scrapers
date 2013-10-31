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
        'biomet.oxfordjournals.org',
        ]
    # Relative name of config file
    config = 'oup.json'

    def getUrlList(self):
        """Get the list of urls from:
        http://www.oxfordjournals.org/help/oxfordjournals.opml.xml"""
        url_list = []
        xml_response = requests.get('http://www.oxfordjournals.org/help/oxfordjournals.opml.xml')
        if xml_response.status_code == 200:
            xml_parse = ElementTree.fromstring(xml_response.text)
            for element in xml_parse.iter():
                if element.attrib.has_key('xmlUrl'):
                    url_list.append(element.attrib['xmlUrl'])
        return url_list

    def clean(self, data):
      data = super(Scraper, self).clean(data)

      data['canonical_url'] = data['source_urls'][0].split(u'?')[0]

      return data

if __name__ == "__main__":
    scraper = Scraper()
    print scraper.getUrlList()

