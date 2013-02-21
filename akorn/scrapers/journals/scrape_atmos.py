import scrape_meta_tags as s

from akorn.scrapers.journals.comm import *
from akorn.scrapers.journals.utils import *

#Current Journals:
#Atmospheric Chemisty and Physics


SCRAPER_DOMAINS = ['www.atmos-chem-phys.net',]



def scrape(abstract_url):

    tree, urls, page_text = get_tree(abstract_url) 

    article = make_blank_article()

    article['title'] = tree.xpath("//span[@class='pb_article_title']")[0].text_content()

    article['abstract'] = tree.xpath("//span[@class='pb_abstract']")[0].text_content()

    article['author_names'] = tree.xpath("//span[@class='pb_authors']")[0].text_content()

    article['scraper'] = 'scrape_atmos'

    info = tree.xpath("//span[@class='pb_citation_header']")[0].text_content()

    info = info.split(',')

 #   article['publisher'] = info

    article['journal'] = info[0]

    article['citation'] = {}
    article['citation']['journal'] = article['journal']
    article['citation']['volume'] = info[1]
    article['citation']['page_first'] = info[-2].split('-')[0]
    article['citation']['page_last'] = info[-2].split('-')[1]
    article['citation']['year'] = info[-1][1:5]


    return article
