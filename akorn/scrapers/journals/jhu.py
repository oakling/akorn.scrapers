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

    def clean(self, data):
        data['abstract'] = data['abstract'].strip()

        # date_published doesn't have a day. let's stick the first of the month in.
        date_str = data.get('date_published')

        if date_str:
            _, _, date_str = date_str.split(',')
            data['date_published'] = '1 ' + date_str.strip()

        data['canonical_url'] = data['source_urls'][-1]

        return super(Scraper, self).clean(data)

