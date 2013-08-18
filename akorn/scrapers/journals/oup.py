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
