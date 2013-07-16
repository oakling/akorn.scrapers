import sys,os.path
import akorn.scrapers.utils
import datetime
import time


#Current Journals:

SCRAPER_DOMAINS = ['oxfordjournals.org',]
    
def scrape(abstract_url):

    tree, urls, page_text = akorn.scrapers.journals.utils.get_tree(abstract_url) 
  
    article = akorn.scrapers.journals.utils.make_blank_article()
    article['scraper'] = 'OUP'
    article['title'] = akorn.scrapers.journals.utils.get_meta('DC.Title', tree)
    article['publisher'] = akorn.scrapers.journals.utils.get_meta('DC.Publisher', tree)
    article['author_names'] = akorn.scrapers.journals.utils.get_meta_list('DC.Contributor', tree)
    article['source_urls'] = [uri for _, uri in urls]
    article['ids'] = {'doi': akorn.scrapers.journals.utils.get_meta('citation_doi', tree)}
    article['journal'] = akorn.scrapers.journals.utils.get_meta('citation_journal_title', tree)
    year,month,day =  akorn.scrapers.journals.utils.get_meta('DC.Date', tree).split('-')
    new_date =  akorn.scrapers.journals.utils.make_datestamp(day, month, year)
    article['date_published'] = new_date
    article['abstract'] = tree.xpath("//div[@class='section abstract']/p")[0].text_content()   
    article['citation']['journal'] =  akorn.scrapers.journals.utils.get_meta('citation_journal_title', tree)
    article['citation']['volume'] =  akorn.scrapers.journals.utils.get_meta('citation_volume', tree)
    article['citation']['page_first'] =  akorn.scrapers.journals.utils.get_meta('citation_firstpage', tree)
    article['citation']['page_last'] =  akorn.scrapers.journals.utils.get_meta('citation_lastpage', tree)
    article['citation']['date'] = akorn.scrapers.journals.utils.get_meta('citation_date', tree)
    #choose the correct date to use here, we only have one so use that
    article['date'] = article['date_published']
  
    return article
