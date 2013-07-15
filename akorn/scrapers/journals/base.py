import lxml
import utils

#decide whether we need the SCRAPER_DOMAIN or whether this is sorted by celery
class BaseScraper():
    """Base class for a web scraper"""

    def make_blank_article(self):
        """"Create a blank article ready to be populated"""
        article = {'scraper': None, 'source_urls': None,'publisher':None,'title': None, 'author_names': None,'ids': None, 'citation': None, 'date': None, 'abstract': None,'journal': None, }
#why do we need year and page in here?
        article['citation'] = { 'journal':None, 'volume': None, 'date': None, 'year': None,'page':None,'page_first': None,'page_last': None }

        return article
        
    def get_config_data_file(self,filepath):
        cdata=lxml.etree.parse(filepath)
        #check this valid xml?
        return cdata
     
    def get_data_item (self,configName,configTree,pageTree):
     #most occasions these appear to be meta tags

        if not (configTree.xpath("//%s/@xPathTag" %configName)[0]=='True'):
            #check for meta tags and meta lists
            if (configTree.xpath("//%s/@metaTag" %configName)[0]=='True'):
                attribute= utils.get_meta(self.get_config_data_value(configName,configTree),pageTree)
            else:
                #must be meta list
                attribute= utils.get_meta_list(self.get_config_data_value(configName,configTree),pageTree)
        else:
            #this is an xpath query
            journalPageTagLocation = self.get_config_data_value(configName,configTree)
            xPathattribute = pageTree.xpath(journalPageTagLocation)   
            #will it always be an individual item or could this be a list?
            attribute=xPathattribute[0].text_content()
        return attribute
         
    def get_config_data_value(self,configItemName,tree):
        searchTermString="//%s/@value" %configItemName
        value = tree.xpath(searchTermString)
        if value:
            return value[0]
        #else:
            #raise an error that we can catch
        
#send in a string that says what the variable is for each element of article
#now we want to take in the config file string and then populate all the fields
    def scrape_article(self, abstract_url=None,fileName=None):
        """Scrape an html page which is an issue of the journal"""
        if abstract_url is None or fileName is None:
            #decide on error to return here instead of none
            return None
        journalTree, urls, page_text = utils.get_tree(abstract_url)
        #create a blank article    
        #article = self.make_blank_article()
        #get the xml config data
        configPageText = self.get_config_data_file(fileName)
        article = {}
        article['source_urls'] =[uri for _, uri in urls]
        for node, parent in utils.iterate_with_parent(configPageText.find('journal')):
            if (len(node)==0):
                 article[node.tag]=node.tag
                #article[node.tag]=self.get_data_item(node.tag, configPageText,journalTree)
            else:  
               if node.tag in article:
				   import pdb;pdb.set_trace();
				   article[parent.tag][node.tag]=node.tag
               else:
				   article[node.tag]={}
               
               
                #article[parent.tag][node.tag] = self.get_data_item(node.tag, configPageText,journalTree)   
        import pdb;pdb.set_trace();
        article['scraper'] = self.get_config_data_value('scraper', configPageText)   
        #over ride the date and ids
        ##think about the best way to do the dates, what if more than one? Probably always overridden
        year,month,day =  article['date_journal'].split('-')
        new_date =  utils.make_datestamp(day, month, year)
        article['date'] = new_date
        article['ids'] ={'doi': article ['ids_journal']} 


        #now fill in the blanks if they are available
        #decide whether or when we fail
        #article['scraper'] = self.get_config_data_value('scraper', configPageText)      
        #article['source_urls'] =[uri for _, uri in urls]
        ##eventually split out all the tags as separate methods so they can be overridden
        #article['publisher'] = self.get_data_item('publisher', configPageText,journalTree)
        #article['title'] = self.get_data_item('title', configPageText,journalTree)
        #article['author_names'] = self.get_data_item('author_names', configPageText,journalTree)
        #article['abstract'] =  self.get_data_item('abstract', configPageText,journalTree)
        #article['journal'] = self.get_data_item('journal', configPageText,journalTree)
        ##think about the best way to do the dates, what if more than one? Probably always overridden
        #year,month,day =  self.get_data_item('date_journal', configPageText,journalTree).split('-')
        #new_date =  utils.make_datestamp(day, month, year)
        #article['date'] = new_date
        #article['citation']['journal'] = self.get_data_item('citation/journal', configPageText,journalTree)
        #article['citation']['volume'] = self.get_data_item('citation/volume', configPageText,journalTree)
        #article['citation']['page_first'] = self.get_data_item('citation/page_first', configPageText,journalTree)
        #article['citation']['page_last'] = self.get_data_item('citation/page_last', configPageText,journalTree)
        #article['citation']['date'] = self.get_data_item('citation/date', configPageText,journalTree)
        #article['ids'] ={'doi': self.get_data_item('ids', configPageText,journalTree)} 
      
        return article
