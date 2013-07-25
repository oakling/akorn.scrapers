import os
import lxml
import urllib2
import utils
import BeautifulSoup

import akorn.scrapers.settings as settings

def lowercase(context, matches):
    """
    Return lowercased input list
    """
    return [bit.lower() for bit in matches]

# Adding lowercase to xpath functions as lxml does not support XPath 2.0
ns = lxml.etree.FunctionNamespace(None)
ns['lowercase'] = lowercase


class BadScraperConfig(Exception):
    pass


class MinimumDataFailure(Exception):
    pass


#decide whether we need the SCRAPER_DOMAIN or whether this is sorted by celery
class BaseScraper(object):
    """Base class for a web scraper"""

    required = [
        'title',
        'author_names',
        'abstract',
        'date_published',
        'journal'
        ]
    get_meta_xpath = lxml.etree.XPath("./head/meta[lowercase(@name)=$name]/@content")

    def __init__(self):
        self.config_data = self.get_config_data_file()


    def fetch_url(self, url):
        """
        Return tuple of urls followed and the final page grabbed
        """
        # Construct request
        req = urllib2.Request(url, headers=utils.headers)
        # Open request and follow redirects to final location of content
        # get_response_chain returns a tuple: urls, page
        return utils.get_response_chain(req)

    def parse_page(self, content, url):
        """
        Return parsed content of given string
        """
        # Force utf-8 encoding by parser
        utf8_parser = lxml.html.HTMLParser(encoding='utf-8')
        # Parse the content and return resulting tree
        return lxml.etree.HTML(content, parser=utf8_parser, base_url=url)

    def get_tree(self, url):
        """
        Return tuple of lxml Element of given url and urls
        followed to get to the final page.
        """
        urls, page = self.fetch_url(url)
        tree = self.parse_page(page.read(), page.geturl())
        return tree, urls

    def get_meta(self, name, source):
        try:
            return self.get_meta_list(name, source)[0]
        except (TypeError, IndexError):
            return None

    def get_meta_list(self, name, source):
        attributes = self.get_meta_xpath(source, name=name.lower())
        if attributes:
            return attributes
        else:
            return None

    def get_config_data_file(self):
        try:
            # Construct path to config file
            filepath = os.path.join(settings.CONFIG_DIR, self.config)
        except AttributeError:
            raise BadScraperConfig('Scraper requires a config property')
        except IOError:
            raise BadScraperConfig('Cannot find config file specified')
        try:
            config = lxml.etree.parse(filepath)
        except lxml.etree.ParseError:
            raise BadScraperConfig('Parsing error in config file')
        # TODO Check config file against DTD?
        return config

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
            attribute = self.get_meta(node_value, source)
        elif node_type == 'metaList':
            attribute = self.get_meta_list(node_value, source)

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
        tree, urls = self.get_tree(abstract_url)
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
                value = self.get_value(node, tree)
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
        # Check that required data is returned
        self.valid(cleaned_article)
        return cleaned_article

    def valid(self, data):
        try:
            # Try to look up each key in the required list
            for key in self.required:
                data[key]
        except KeyError:
            raise MinimumDataFailure('Required property, {}, missing'.format(key))
        return True

    def clean(self, data):
        return data
