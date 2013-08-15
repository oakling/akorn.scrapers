from akorn.scrapers.journals.scrape_meta_tags import scrape_tree as meta_scrape_tree

from akorn.scrapers.utils import *

#Current Journals:
#Proceedings of the National Academy of Sciences


SCRAPER_DOMAINS = ['www.pnas.org']



def scrape(abstract_url):

    tree, urls, page_text = get_tree(abstract_url) 

    article = meta_scrape_tree(tree, urls, page_text)

    #For P.R.C:A and P.R.C:B
    #For P.L.O.S
    if article['journal'] == 'Proceedings of the National Academy of Sciences':

        article['abstract'] = tree.xpath("//div[@class='section abstract']/p")[0].text_content()


    return article




    
