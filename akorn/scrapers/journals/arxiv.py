import feedparser
import re
import requests
import time

from akorn.scraper.base import BaseScraper

class Scraper(BaseScraper):
    # Should be scraped at 10 past midnight
    schedule = {"minute" :10, "hour": "0"}
    # The url for the arxiv API
    base_url = 'http://export.arxiv.org/api/query'
    # List of feeds that scraper is for
    feeds = [
        'http://export.arxiv.org/rss/astro-ph',
        'http://export.arxiv.org/rss/cond-mat',
        'http://export.arxiv.org/rss/cs',
        'http://export.arxiv.org/rss/gr-qc',
        'http://export.arxiv.org/rss/hep-ex',
        'http://export.arxiv.org/rss/hep-lat',
        'http://export.arxiv.org/rss/hep-ph',
        'http://export.arxiv.org/rss/hep-th',
        'http://export.arxiv.org/rss/math',
        'http://export.arxiv.org/rss/math-ph',
        'http://export.arxiv.org/rss/nlin',
        'http://export.arxiv.org/rss/nucl-ex',
        'http://export.arxiv.org/rss/nucl-th',
        'http://export.arxiv.org/rss/physics',
        'http://export.arxiv.org/rss/q-bio',
        'http://export.arxiv.org/rss/q-fin',
        'http://export.arxiv.org/rss/quant-ph',
        'http://export.arxiv.org/rss/stat',
        ]
    # List of domains that scraper is for
    domains = [
        'www.arxiv.org',
        'arxiv.org',
        ]

    @classmethod
    def arxiv_id(cls, url):
        return cls.remove_vNumber(re.search('(?:abs|pdf)/(.*)', url).groups()[0])

    @staticmethod
    def remove_vNumber(s):
        return re.sub(r'v[0-9]+', '', s)

    def query_arxiv(self, arxiv_id):
        # Make API call
        response = requests.get(self.base_url, params={'id_list': arxiv_id})
        # Parse response
        result = feedparser.parse(response.text)['items'][0]
        # Transpose response to the values we need
        return {
            'title': result.get('title'),
            'author_names': [author.name for author in result.authors],
            'abstract': result.get('summary'),
            'date_revised': time.mktime(result.get('updated_parsed')),
            'date_published': time.mktime(result.get('published_parsed')),
            'date_scraped': int(time.time())
            'arxiv': arxiv_id,
            'source_urls': [self.remove_vNumber(result.get('link'))],
            'journal': 'arxiv:' + result.arxiv_primary_category['term'],
            'doi': result.get('arxiv_doi')
        }

    def scrape_article(self, url):
        # Convert the URL from the feed into an arxiv ID
        arxiv_id = self.arxiv_id(url)
        # Query the arxiv API for the article ID
        article = self.query_arxiv(arxiv_id)
        # Check no properties have been set to None
        self.valid(article)
        return article
