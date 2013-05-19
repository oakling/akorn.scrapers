
import utils
import os
#decide whether we need the SCRAPER_DOMAIN or whether this is sorted by celery
class BaseScraper():
    """Base class for a web scraper"""

    def make_blank_article(self):
        """"Create a blank article ready to be populated"""
        article = {'scraper': None, 'source_urls': None,'publisher':None,'title': None, 'author_names': None,
               'ids': None, 'citation': None, 'date': None, 'abstract': None,
               'journal': None, }

        article['citation'] = { 'journal':None, 'volume': None, 'year': None, 'page_first': None,'page_last': None }

        return article
        
    def get_config_data_file(filepath):
        xmlFile = os.open(filepath)
        cdata = xmlFile.read()
        xmlFile.close()
        #check this valid xml?
        return data
     
    def get_data_item (configName,configTree,pageTree):
     #most occasions these appear to be meta tags
        try:
          if not configTree.xpath("//'%s'/@xPathTag" %configName).text_content():
			#check for meta tags and meta lists
			if configTree.xpath("//'%s'/@metaTag" %configName).text_content():
				attribute= get_meta(self.get_config_data_value(configName,pageTree),pageTree)
			else:
				#must be meta list
				attribute= get_meta_list(self.get_config_data_value(configName,pageTree),pageTree)
          else:
			#this is an xpath query
			journalXPath = self.get_config_data_value(configName,pageTree)
			attribute = tree.xpath(journalXPath).text_content()    
          if attribute:
           return attribute[0]
          else:
           return None
        except:
         return None
        pass
        
    def get_config_data_value(configItemName,tree):
         value = tree.xpath("//'%s'/@value" %configItemName).text_content() 
         if value:
           return value[0]
       
        
    
        
        
#send in a string that says what the variable is for each element of article
     #now we want to take in the config file string and then populate all the fields
    def scrape_article(self, abstract_url=None,fileName=None):
        """Scrape a html page which is an issue of the journal"""
        if abstract_url is None or fileName is None:
            return None
        journalTree, urls, page_text = utils.get_tree(abstract_url)
    #create a blank article    
        article = self.make_blank_article()
    #get the xml config data
        configPageText = self.get_config_data_file(fileName)
     #now fill in the blanks if they are available
     #decide whether or when we fail
        article['scraper'] = get_config_data_value('scraper', configPageText)      
        article['source_urls'] =[uri for _, uri in urls]
     #eventually split out all the tags as separate methods so they can be overridden
        article['publisher'] = get_data_item('publisher', configPageText,journalTree)
        article['title'] = get_data_item('publisher', configPageText,journalTree)
        article['author_names'] = get_data_item('author_names', configPageText,journalTree)
        article['abstract'] =  get_data_item('abstract', configPageText,journalTree)
        article['journal'] = get_data_item('journal', configPageText,journalTree)
	#think about how to do the dates
        year,month,day =  get_data_item('date', configPageText,journalTree)
        new_date =  akorn.scrapers.journals.utils.make_datestamp(day, month, year)
        article['date'] = new_date

        configPageTextCitation = configPageText.xpath('//citation')
        article['citation']['journal'] = get_data_item('journal', configPageTextCitation,journalTree)
        article['citation']['volume'] = get_data_item('volume', configPageTextCitation,journalTree)
        article['citation']['page_first'] = get_data_item('page_first', configPageTextCitation,journalTree)
        article['citation']['page_last'] = get_data_item('page_last', configPageTextCitation,journalTree)
        article['citation']['year'] = get_data_item('year', configPageTextCitation,journalTree)
        article['ids'] ={'doi': get_data_item('ids', configPageTextCitation,journalTree)}
        return article
