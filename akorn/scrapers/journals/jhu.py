from akorn.scrapers.base import BaseScraper

class Scraper(BaseScraper):
    # List of feeds that scraper is for
    feeds = [
        'http://feeds.muse.jhu.edu/journals/american_journal_of_mathematics/latest_articles.xml'
        ]
    # Should be scraped every hour
    schedule = {"minute": 1, "hour": "*"}
    # List of domains that scraper is for
    domains = [
        'muse.jhu.edu',
        ]
    # Relative name of config file
    config = 'jhu.json'

    def clean(self, article):
        date_str = article.get('date_published')
        if date_str:
            _, _, date_str = date_str.split(',')
            article['date_published'] = '1 '+date_str.strip()

        return super(Scraper, self).clean(article)
