from .scrape_meta_tags import scrape_tree as meta_scrape_tree

from akorn.scrapers.utils import *

#Current Journals:
#Proceedings of the Royal Society A & B


SCRAPER_DOMAINS = ['rspb.royalsocietypublishing.org',
                   'rspa.royalsocietypublishing.org']



def scrape(abstract_url):

    tree, urls, page_text = get_tree(abstract_url) 

    article = meta_scrape_tree.scrape_tree(tree, urls, page_text)

    #For P.R.C:A and P.R.C:B
    if article['journal'] == 'Proceedings of the Royal Society A: \
Mathematical, Physical and Engineering Science' or\
    article['journal'] == 'Proceedings of the Royal Society B: \
Biological Sciences':

        article['abstract'] = tree.xpath("//div[@class='section abstract']/p")[0].text_content()


    return article




    
