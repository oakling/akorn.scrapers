from akorn.scrapers.base import BaseScraper

class Scraper(BaseScraper):
    # List of feeds that scraper is for
    # TODO Lots more here: http://www.oxfordjournals.org/subject/mathematics/
    feeds = [
        "feed://onlinelibrary.wiley.com/rss/journal/10.1111/(ISSN)1365-2966",
        "feed://onlinelibrary.wiley.com/rss/journal/10.1111/(ISSN)1745-3933",
        "feed://onlinelibrary.wiley.com/rss/journal/10.1002/(ISSN)1099-1476",
        "feed://onlinelibrary.wiley.com/rss/journal/10.1002/(ISSN)1521-4095",
        "feed://onlinelibrary.wiley.com/rss/journal/10.1111/(ISSN)1365-246X",
        "feed://onlinelibrary.wiley.com/rss/journal/10.1111/(ISSN)1945-5100",
        "feed://onlinelibrary.wiley.com/rss/journal/10.1002/(ISSN)1521-3994",
        "feed://onlinelibrary.wiley.com/rss/journal/10.1002/(ISSN)1530-261X",
        "feed://onlinelibrary.wiley.com/rss/journal/10.1002/(ISSN)1864-0648",
        "feed://onlinelibrary.wiley.com/rss/journal/10.1002/(ISSN)1477-870X",
        "feed://onlinelibrary.wiley.com/rss/journal/10.1002/(ISSN)1616-3028",
        "feed://onlinelibrary.wiley.com/rss/journal/10.1002/(ISSN)1613-6829",
        "http://onlinelibrary.wiley.com/rss/journal/10.1002/(ISSN)2192-2659",
        "feed://onlinelibrary.wiley.com/rss/journal/10.1002/(ISSN)1860-7314",
        "feed://onlinelibrary.wiley.com/rss/journal/10.1002/(ISSN)1099-0682c",
        "feed://onlinelibrary.wiley.com/rss/journal/10.1111/(ISSN)1365-2818",
        "feed://onlinelibrary.wiley.com/rss/journal/10.1002/(ISSN)1439-7633",
        "feed://onlinelibrary.wiley.com/rss/journal/10.1002/(ISSN)1439-7641",
        "feed://onlinelibrary.wiley.com/rss/journal/10.1002/(ISSN)1614-6840",
        "feed://onlinelibrary.wiley.com/rss/journal/10.1002/(ISSN)1097-0312",
        ]
    # List of domains that scraper is for
    domains = [
        'onlinelibrary.wiley.com',
        ]
    # Relative name of config file
    config = 'wiley.json'

    def clean(self, article):
        article = super(Scraper, self).clean(article)

        # For some reason Wiley appends session ids, that need to be stripped out
        article['source_urls'] = [url.split(';')[0] for url in article.get('source_urls', [])]

        return article
