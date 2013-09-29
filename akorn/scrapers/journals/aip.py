from akorn.scrapers.base import BaseScraper
from dateutil import parser
import datetime
import time

class Scraper(BaseScraper):
    # List of feeds that scraper is for
    feeds = ['http://aipadvances.aip.org/search_rss?key=AAIDBI&societykey=AIP&coden=AAIDBI&q=+&displayid=AIP&sortby=newestdate&faceted=faceted&sortby=newestdate&CP_Style=false&alias=&searchzone=2&rss=rss&rsstitle=AIP%20Advances:%20ALL%20TOPICS',
             'http://scitation.aip.org/rss/apl1.xml',
             'http://scitation.aip.org/rss/bmf.xml',
             'http://scitation.aip.org/rss/chaos1.xml',
             'http://scitation.aip.org/rss/jap1.xml',
             'http://scitation.aip.org/rss/jcp1.xml',
             'http://jla.aip.org/search_rss?q=&key=JLAPEN&fromvolume=22&fromissue=3&tovolume=present&toissue=present&sortby=newestdate&recordspage=20&rss=rss&rsstitle=Journal%20of%20Laser%20Applications',
             'http://scitation.aip.org/rss/jmp1.xml',
             'http://scitation.aip.org/rss/jpcrd1.xml',
             'http://scitation.aip.org/rss/jrse.xml',
             'http://scitation.aip.org/rss/ltp1.xml',
             'http://scitation.aip.org/rss/pof1.xml',
             'http://scitation.aip.org/rss/php1.xml',
             'http://scitation.aip.org/rss/rsi1.xml',
             'http://taml.aip.org/search_rss?q=+&searchtype=searchin&key=TAMLBX&sortby=newestdate&recordspage=25&rss=rss&rsstitle=Theoretical%20and%20Applied%20Mechanics%20Letters%20from%20ALL%20TOPICS',
             'http://apl-oep.aip.org/search_rss?q=+&searchtype=searchin&searchzone=2&ignoredates=true&key=APLOEP&sortby=newestdate&recordspage=25&possible1=&possible1zone=article&bool1=and&submit1=Search&rss=rss&rsstitle=OEP:%20ALL%20TOPICS',
             'http://apr.aip.org/search_rss?q=+&searchtype=searchin&searchzone=2&ignoredates=true&key=JAPAPR&sortby=newestdate&recordspage=25&possible1=&possible1zone=article&bool1=and&submit1=Search&rss=rss&rsstitle=APR:%20ALL%20TOPICS',
             'http://jcp-bcp.aip.org/search_rss?q=+&searchtype=searchin&searchzone=2&ignoredates=true&key=JCPBCP&sortby=newestdate&recordspage=25&possible1=&possible1zone=article&bool1=and&submit1=Search&rss=rss&rsstitle=BCP:%20ALL%20TOPICS',
             ]

    # Where to find the URL in each feed item
    feed_tag = 'link'

    # List of domains that scraper is for
    domains = ['aipadvances.aip.org','aplmaterials.aip.org', 'apl.aip.org', 'bmf.aip.org', 'chaos.aip.org', 'cjcp.aip.org', 'jap.aip.org', 'jcp.aip.org', 'jla.aip.org', 'jmp.aip.org', 'jpcrd.aip.org', 'jrse.aip.org', 'ltp.aip.org', 'pof.aip.org', 'pop.aip.org', 'rsi.aip.org', 'sd.aip.org', 'taml.aip.org', 'apl-oep.aip.org', 'apr.aip.org', 'jcp-bcp.aip.org']

    # Relative name of config file
    config = 'aip.json'

    def clean(self, data):
        data['doi'] = data['doi'][4:]

        #2013-09-25
        year, month, day = map(int, data['date_published'].split('-'))
        data['date_published'] = time.mktime(datetime.date(year, month, day).timetuple())

        return data

