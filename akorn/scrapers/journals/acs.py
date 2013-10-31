from akorn.scrapers.base import BaseScraper

from dateutil import parser
import time

class Scraper(BaseScraper):
    # List of feeds that scraper is for
    feeds = ['http://feeds.feedburner.com/acs/achre4',
             'http://feeds.feedburner.com/acs/aamick',
             'http://feeds.feedburner.com/acs/accacs',
             'http://feeds.feedburner.com/acs/acbcct',
             'http://feeds.feedburner.com/acs/acncdm',
             'http://feeds.feedburner.com/acs/acsccc',
             'http://feeds.feedburner.com/acs/amlccd',
             'http://feeds.feedburner.com/acs/amclct',
             'http://feeds.feedburner.com/acs/ancac3',
             'http://feeds.feedburner.com/acs/ascecg',
             'http://feeds.feedburner.com/acs/asbcd6',
             'http://feeds.feedburner.com/acs/ancham',
             'http://feeds.feedburner.com/acs/bichaw',
             'http://feeds.feedburner.com/acs/bcches',
             'http://feeds.feedburner.com/acs/bomaf6',
             'http://feeds.feedburner.com/acs/crtoec',
             'http://feeds.feedburner.com/acs/chreay',
             'http://feeds.feedburner.com/acs/cmatex',
             'http://feeds.feedburner.com/acs/cgdefu',
             'http://feeds.feedburner.com/acs/enfuem',
             'http://feeds.feedburner.com/acs/esthag',
             'http://feeds.feedburner.com/acs/estlcu',
             'http://feeds.feedburner.com/acs/iecred',
             'http://feeds.feedburner.com/acs/inocaj',
             'http://feeds.feedburner.com/acs/jacsat',
             'http://feeds.feedburner.com/acs/jafcau',
             'http://feeds.feedburner.com/acs/jceaax',
             'http://feeds.feedburner.com/acs/jceda8',
             'http://feeds.feedburner.com/acs/jcisd8',
             'http://feeds.feedburner.com/acs/jctcce',
             'http://feeds.feedburner.com/acs/jmcmar',
             'http://feeds.feedburner.com/acs/jnprdf',
             'http://feeds.feedburner.com/acs/joceah',
             'http://feeds.feedburner.com/acs/jpcafh',
             'http://feeds.feedburner.com/acs/jpcbfk',
             'http://feeds.feedburner.com/acs/jpccck',
             'http://feeds.feedburner.com/acs/jpclcd',
             'http://feeds.feedburner.com/acs/jprobs',
             'http://feeds.feedburner.com/acs/langd5',
             'http://feeds.feedburner.com/acs/mamobx',
             'http://feeds.feedburner.com/acs/mpohbp',
             'http://feeds.feedburner.com/acs/nalefd',
             'http://feeds.feedburner.com/acs/orlef7',
             'http://feeds.feedburner.com/acs/oprdfk',
             'http://feeds.feedburner.com/acs/orgnd7',]

    # Where to find the URL in each feed item
    feed_tag = ['feedburner_origlink', 'link']

    # List of domains that scraper is for
    domains = ['pubs.acs.org']

    # Relative name of config file
    config = 'acs.json'

