import feedparser
import random
import urllib2
import sys
from akorn.scrapers import scrapers

ss = scrapers.Scrapers()

feeds = ss.feeds.items()
random.shuffle(feeds)

if len(sys.argv) > 1:
  check_module_name = sys.argv[1]
else:
  check_module_name = None

for module_name, (feed_tag, feed_urls) in feeds:
  if check_module_name is not None and check_module_name != module_name:
    continue

  print "Module: {}".format(module_name)

  for feed_url in feed_urls:
    print "  Feed: {}".format(feed_url)
    response = feedparser.parse(feed_url)

    try:
      item = random.choice(response['items'])
    except IndexError:
      print "      Empty feed."
      continue

    if type(feed_tag) is list:
      for feed_tag_ in feed_tag:
        if feed_tag_ in item:
          item_url = item[feed_tag_]
          break
      else:
        raise Exception("Feed tag(s) not valid.")
    else:
      item_url = item[feed_tag]
    
    print "      Scraping url: {}".format(item_url)

    _, scrape_function = ss.resolve_scraper(item_url)

    try:
      scraped_doc = scrape_function(item_url)
    except urllib2.HTTPError, e:
      print e
    else:
      print "      ", scraped_doc

