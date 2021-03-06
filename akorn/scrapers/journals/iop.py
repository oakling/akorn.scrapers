from akorn.scrapers.base import BaseScraper

class Scraper(BaseScraper):
    # List of feeds that scraper is for
    feeds = [
        "http://iopscience.iop.org/1538-3881/?rss=1",
        "http://iopscience.iop.org/1538-4357/?rss=1",
        "http://iopscience.iop.org/0067-0049/?rss=1",
        "http://iopscience.iop.org/1748-3190/?rss=1",
        "http://iopscience.iop.org/1748-605X/?rss=1",
        "http://iopscience.iop.org/1009-9271/?rss=1",
        "http://iopscience.iop.org/1674-0068/?rss=1",
        "http://iopscience.iop.org/1674-1056/?rss=1",
        "http://iopscience.iop.org/0256-307X/?rss=1",
        "http://iopscience.iop.org/0264-9381/?rss=1",
        "http://iopscience.iop.org/0295-5075/?rss=1",
        "http://iopscience.iop.org/1748-9326/?rss=1",
        "http://iopscience.iop.org/0143-0807/?rss=1",
        "http://iopscience.iop.org/0266-5611/?rss=1",
        "http://iopscience.iop.org/1752-7163/?rss=1",
        "http://iopscience.iop.org/1475-7516/?rss=1",
        "http://iopscience.iop.org/1742-2140/?rss=1",
        "http://iopscience.iop.org/1126-6708/?rss=1",
        "http://iopscience.iop.org/1748-0221/?rss=1",
        "http://iopscience.iop.org/0960-1317/?rss=1",
        "http://iopscience.iop.org/1741-2552/?rss=1",
        "http://iopscience.iop.org/1464-4258/?rss=1",
        "http://iopscience.iop.org/0305-4470/?rss=1",
        "http://iopscience.iop.org/1751-8121/?rss=1",
        "http://iopscience.iop.org/0953-4075/?rss=1",
        "http://iopscience.iop.org/0022-3727/?rss=1",
        "http://iopscience.iop.org/0954-3899/?rss=1",
        "http://iopscience.iop.org/0953-8984/?rss=1",
        "http://iopscience.iop.org/1742-6596/?rss=1",
        "http://iopscience.iop.org/0952-4746/?rss=1",
        "http://iopscience.iop.org/1742-5468/?rss=1",
        "http://iopscience.iop.org/0957-0233/?rss=1",
        "http://iopscience.iop.org/0026-1394/?rss=1",
        "http://iopscience.iop.org/0965-0393/?rss=1",
        "http://iopscience.iop.org/0957-4484/?rss=1",
        "http://iopscience.iop.org/1367-2630/?rss=1",
        "http://iopscience.iop.org/0951-7715/?rss=1",
        "http://iopscience.iop.org/0029-5515/?rss=1",
        "http://iopscience.iop.org/1402-4896/?rss=1",
        "http://iopscience.iop.org/1478-3975/?rss=1",
        "http://iopscience.iop.org/0031-9120/?rss=1",
        "http://iopscience.iop.org/0031-9155/?rss=1",
        "http://iopscience.iop.org/0967-3334/?rss=1",
        "http://iopscience.iop.org/0741-3335/?rss=1",
        "http://iopscience.iop.org/1009-0630/?rss=1",
        "http://iopscience.iop.org/0963-0252/?rss=1",
        "http://iopscience.iop.org/0034-4885/?rss=1",
        "http://iopscience.iop.org/0268-1242/?rss=1",
        "http://iopscience.iop.org/0964-1726/?rss=1",
        "http://iopscience.iop.org/0953-2048/?rss=1",
        "http://iopscience.iop.org/0004-637X/?rss=1",
        ]
    # List of domains that scraper is for
    domains = [
        'iopscience.iop.org',
        ]
    # Relative name of config file
    config = 'iop.json'


