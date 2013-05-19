import sys,os.path
import akorn.scrapers.journals.utils
import datetime
import time

from akorn.scrapers.journals.base import BaseScraper
#Current Journals:

SCRAPER_DOMAINS = ['oxfordjournals.org',]
class ScraperOUP(BaseScraper):
    """Scrape OUP"""



def scrape(abstract_url,configFilePath=None):
    """Scrape an article level url and return an article dict"""
    scraper = ScraperOUP()
    article = scraper.scrape_article(abstract_url,configFilePath)
    return article
    
