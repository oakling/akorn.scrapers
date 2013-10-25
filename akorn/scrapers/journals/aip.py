from akorn.scrapers.base import BaseScraper
from dateutil import parser
import datetime
import time

class Scraper(BaseScraper):
    # List of feeds that scraper is for
    feeds = ['http://scitation.aip.org/rss/content/asa/journal/atdy/latestarticles?fmt=rss',
'http://scitation.aip.org/rss/content/aip/journal/adva/latestarticles?fmt=rss',
'http://scitation.aip.org/rss/content/aapt/journal/ajp/latestarticles?fmt=rss',
'http://scitation.aip.org/rss/content/aip/journal/aplmater/latestarticles?fmt=rss',
'http://scitation.aip.org/rss/content/aip/journal/aploep/latestarticles?fmt=rss',
'http://scitation.aip.org/rss/content/aip/journal/apl/latestarticles?fmt=rss',
'http://scitation.aip.org/rss/content/aip/journal/apr/latestarticles?fmt=rss',
'http://scitation.aip.org/rss/content/aas/journal/aer/latestarticles?fmt=rss',
'http://scitation.aip.org/rss/content/aip/journal/bmf/latestarticles?fmt=rss',
'http://scitation.aip.org/rss/content/aip/journal/chaos/latestarticles?fmt=rss',
'http://scitation.aip.org/rss/content/cps/journal/cjcp/latestarticles?fmt=rss',
'http://scitation.aip.org/rss/content/aip/journal/cise/latestarticles?fmt=rss',
'http://scitation.aip.org/rss/content/asa/journal/jasael/latestarticles?fmt=rss',
'http://scitation.aip.org/rss/content/aip/journal/jcpbio/latestarticles?fmt=rss',
'http://scitation.aip.org/rss/content/aip/journal/jap/latestarticles?fmt=rss'
'http://scitation.aip.org/rss/content/aip/journal/jcp/latestarticles?fmt=rss',
'http://scitation.aip.org/rss/content/aip/journal/jmp/latestarticles?fmt=rss',
'http://scitation.aip.org/rss/content/aip/journal/jpcrd/latestarticles?fmt=rss',
'http://scitation.aip.org/rss/content/aip/journal/jrse/latestarticles?fmt=rss',
'http://scitation.aip.org/rss/content/sor/journal/jor2/latestarticles?fmt=rss',
'http://scitation.aip.org/rss/content/asa/journal/jasa/latestarticles?fmt=rss',
'http://scitation.aip.org/rss/content/avs/journal/jvsta/latestarticles?fmt=rss',
'http://scitation.aip.org/rss/content/avs/journal/jvstb/latestarticles?fmt=rss',
'http://scitation.aip.org/rss/content/aip/journal/ltp/latestarticles?fmt=rss',
'http://scitation.aip.org/rss/content/aapm/journal/medphys/latestarticles?fmt=rss',
'http://scitation.aip.org/rss/content/aip/journal/pof2/latestarticles?fmt=rss',
'http://scitation.aip.org/rss/content/aip/journal/pop/latestarticles?fmt=rss',
'http://scitation.aip.org/rss/content/aapt/journal/tpt/latestarticles?fmt=rss',
'http://scitation.aip.org/rss/content/asa/journal/poma/latestarticles?fmt=rss',
'http://scitation.aip.org/rss/content/aip/journal/rsi/latestarticles?fmt=rss',
'http://scitation.aip.org/rss/content/aca/journal/sdy/latestarticles?fmt=rss',
'http://scitation.aip.org/rss/content/avs/journal/sss/latestarticles?fmt=rss',
'http://scitation.aip.org/rss/content/cstam/journal/taml/latestarticles?fmt=rss',
             ]

    # Where to find the URL in each feed item
    feed_tag = 'link'

    # List of domains that scraper is for
    domains = ['aipadvances.aip.org','aplmaterials.aip.org', 'apl.aip.org', 'bmf.aip.org', 'chaos.aip.org', 'cjcp.aip.org', 'jap.aip.org', 'jcp.aip.org', 'jla.aip.org', 'jmp.aip.org', 'jpcrd.aip.org', 'jrse.aip.org', 'ltp.aip.org', 'pof.aip.org', 'pop.aip.org', 'rsi.aip.org', 'sd.aip.org', 'taml.aip.org', 'apl-oep.aip.org', 'apr.aip.org', 'jcp-bcp.aip.org', 'link.aip.org', 'scitation.aip.org']

    # Relative name of config file
    config = 'aip.json'

    def clean(self, data):
        #2013/09/25
        year, month, day = map(int, data['date_published'].split('/'))
        data['date_published'] = time.mktime(datetime.date(year, month, day).timetuple())

        return data

