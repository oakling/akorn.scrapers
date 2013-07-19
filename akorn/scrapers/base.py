import os
import lxml
import utils

import akorn.scrapers.settings as settings


class BadScraperConfig(Exception):
    pass


#decide whether we need the SCRAPER_DOMAIN or whether this is sorted by celery
class BaseScraper(object):
    """Base class for a web scraper"""

    def __init__(self):
        if not self.config:
            raise BadScraperConfig('Scraper requires a config property')
        self.config_data = self.get_config_data_file()
        
    def get_config_data_file(self):
        # Construct path to config file
        filepath = os.path.join(settings.CONFIG_DIR, self.config)
        # TODO Check for parse errors
        # TODO Check config file against DTD?
        return lxml.etree.parse(filepath)

    def get_value(self, node, source):
        # Get the type of node
        node_type = node.get('type')
        # Get the value to look in source for
        node_value = node.get('value')
        attribute = None
        if node_type == 'xPathTag':
            found = source.xpath(node_value)
            if found:
                attribute = found[0].text_content()
        elif node_type == 'css':
            found = source.cssselect(node_value)
            if found:
                attribute = found[0].text_content()
        elif node_type == 'metaTag':
            attribute = utils.get_meta(node_value, source)
        elif node_type == 'metaList':
            attribute = utils.get_meta_list(node_value, source)

        if not attribute:
            attribute = ''

        return attribute
         
    def get_config_data_value(self,configItemName,tree):
        searchTermString="//%s/@value" %configItemName
        value = tree.xpath(searchTermString)
        if value:
            return value[0]
        #else:
            #raise an error that we can catch

    def scrape_article(self, abstract_url):
        """Scrape an html page which is an issue of the journal"""
        journalTree, urls, page_text = utils.get_tree(abstract_url)
        # Get the xml config data
        config_data = self.config_data
        # Create the empty article dict
        article = {}
        # Walk over config data, populating article
        for node, parent in utils.iterate_with_parent(config_data.find('journal')):
            # If there are child nodes, then create a containing dict
            if len(node):
                article[node.tag] = {}
            else:
                # Get the value from the source document
                value = self.get_value(node, journalTree)
                # If no value is found then skip
                if not value:
                    continue
	        if parent is None:
		    article[node.tag] = value
	        else:
		    article[parent.tag][node.tag] = value
        # Add meta data
        article['source_urls'] = [uri for _, uri in urls]
        # Run cleaning methods over article data
        cleaned_article = self.clean(article)
        # TODO Check for minimum data returned
        return cleaned_article

    def clean(self, data):
        data['ids'] = {'doi': data['citation']['ids_journal']}
        return data
