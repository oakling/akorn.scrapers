from akorn.scrapers.base import BaseScraper

from datetime import datetime
import time

class Scraper(BaseScraper):
    # List of feeds that scraper is for
    feeds = [
                (
                    "http://www.atmos-chem-phys.net/xml/rss2_0.xml",
                    "link",
                    {"minute":1, "hour": "15"},
                )
            ]
    # List of domains that scraper is for
    domains = ['www.atmos-chem-phys.net']
    # Relative name of config file
    config = 'atmos.json'

    def clean(self, article):
        article = super(Scraper, self).clean(article)

        # Clean up DOI value
        doi = article.get('doi')
        if doi:
            # First 4 chars are "doi:"
            article['doi'] = doi[3:]
        return article
