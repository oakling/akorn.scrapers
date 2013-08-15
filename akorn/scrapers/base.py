import functools
import json
import lxml
from lxml.cssselect import CSSSelector
import os
import urllib2

import akorn.scrapers.utils as utils
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


class Config(object):
    meta_xpath_sel = lxml.etree.XPath("./head/meta[lowercase(@name)=$name]/@content")
    lookup_types = {
            'xPathTag': 'compile_xpath',
            'css': 'compile_css',
            'metaTag': 'compile_meta_single',
            'metaList': 'compile_meta'
        }
    # TODO: Check for required values in config supplied
    required = [
        'title',
        'author_names',
        'abstract',
        'date_published',
        'journal'
        ]
    optional = [
        'doi',
        'volume',
        'issue',
        'pages',
        'publisher'
        ]

    def __init__(self, filename=None):
        #  If a file is provided, then try to parse and load it
        if filename:
            path = self.get_filepath(filename)
            config_content = self.fetch_config(path)
            parsed = self.parse_config(config_content)
            self.config = self.compile_config(parsed)
            self.validate(self.config)

    @property
    def allowed(self):
        return self.required+self.optional

    @property
    def not_allowed(self):
        allowed = self.allowed
        return [key for key in self.config.keys() if not key in allowed]

    @property
    def unused(self):
        """
        Return list of allowed properties not used in the config
        """
        config = self.config
        return [key for key in self.allowed if not key in config.keys()]

    @property
    def missing(self):
        """
        Return list of missing required properties
        """
        return [key for key in self.unused if key in self.required]

    def check_allowed(self, config):
        """
        Raises BadScraperConfig if unknown properties are found
        """
        not_allowed = self.not_allowed
        if not_allowed:
            raise BadScraperConfig("Unknown properties: {}".format(', '.join(not_allowed)))

    def check_required(self):
        """
        Raises BadScraperConfig if required properties are not found
        """
        missing = self.missing
        if missing:
            raise BadScraperConfig("Required properties: {}".format(', '.join(missing)))

    def validate(self, config):
        self.check_required(config)
        self.check_allowed(config)

    def parse_xml(self, xml_tree):
        """
        Return config dict based on provided XML tree
        """
        config = {}
        # Walk over xml config data, populating config structure
        for node, parent in utils.iterate_with_parent(xml_tree.find('journal')):
            # If there are child nodes, then create a containing dict
            if len(node):
                config[node.tag] = {}
            else:
                # Get the value from the source document
                value = [{
                    'type': node.get('type'),
                    'value': node.get('value')
                    }]
                # If no value is found then skip
                if not value:
                    continue
                if parent is None:
                    config[node.tag] = value
                else:
                    config[parent.tag][node.tag] = value
        return config

    def compile_config(self, config):
        """
        Walk over configuration and replace values with functions
        """
        return utils.walk_and_apply(config, self.compile_lookups)

    def compile_lookups(self, items, **kwargs):
        """
        Return list of given lookups converted to the associated functions
        """
        return [self.compile_lookup(item) for item in items]

    def compile_lookup(self, item):
        """
        Return the function for the given lookup
        """
        # Get the type of the lookup
        lookup_type = item.get('type', '')
        # Find the associated function
        compile_func = getattr(self, self.lookup_types[lookup_type])
        # Wrap the function with the lookup as its first parameter
        return compile_func(item)

    def fetch_config(self, config_filepath):
        """
        Return the contents of the given filepath
        """
        with open(config_filepath, 'r') as fh:
            return fh.read()

    def parse_config(self, config_file_contents):
        """
        Return dict representing parsed contents of given file
        """
        try:
            # Try to load config file, assuming JSON
            return json.loads(config_file_contents)
        except ValueError:
            try:
                # If that fails, try XML instead
                xml_config = lxml.etree.fromstring(config_file_contents)
                # Convert it to the standard representation
                return self.parse_xml(xml_config)
            except lxml.etree.ParseError:
                raise BadScraperConfig('Parsing error in config')

    # TODO Use of settings constant in method inappropriate
    def get_filepath(self, filename):
        """
        Return full path to config file for the given filename
        """
        # Construct path to config file
        filepath = os.path.join(settings.CONFIG_DIR, filename)
        return filepath

    def call_selector(self, selector, lookup, source, **kwargs):
        """
        Return output from evaluating given selector against the given source
        """
        found = selector(source, **kwargs)
        # TODO Should be done after down-selection to single
        cleaned = self.clean_selector_output(found)
        try:
            if lookup.get('single'):
                out = cleaned[0]
            else:
                out = cleaned
        except IndexError:
            return None
        # If value not found, then return None
        if not out:
            return None
        return out

    def clean_selector_output(self, output):
        clean = []
        for item in output:
            if isinstance(item, lxml.html.HtmlElement):
                clean.append(lxml.html.tostring(item))
            else:
                clean.append(item)
        return clean

    def bind_selector(self, *args, **kwargs):
        """
        Return self.call_selector wrapped with supplied arguments
        """
        return functools.partial(self.call_selector, *args, **kwargs)

    def compile_xpath(self, lookup):
        """
        Return callable compiled xpath selector
        """
        sel = lxml.XPath(lookup.get('value', ''))
        return self.bind_selector(sel, lookup)

    def compile_css(self, lookup):
        """
        Return callable compiled css selector
        """
        sel = CSSSelector(lookup.get('value', ''))
        return self.bind_selector(sel, lookup)

    def compile_meta_single(self, lookup):
        """
        Return callable compiled xpath meta tag selector, limited to 1 value
        """
        lookup['single'] = True
        return self.compile_meta(lookup)

    def compile_meta(self, lookup):
        """
        Return callable compiled xpath meta tag selector
        """
        name = lookup.get('value', '')
        return self.bind_selector(
            self.meta_xpath_sel,
            lookup,
            name=name.lower())

    def lookup_value(self, source, firstof, **kwargs):
        """
        Return the value of the first successful lookup
        """
        # Try each of the lookups in turn
        for lookup in firstof:
            # Call the lookup function, passing it the article source
            value = lookup(source)
            if value:
                # Finish as soon as we find a value
                return value
        return None

    def map_to_config(self, source):
        """
        Return dict of values extracted from given source based on self.config
        """
        # Curry the lookup_value function with the source tree
        func = functools.partial(self.lookup_value, source)
        # Apply the curried function to the config dict
        return utils.walk_and_apply(self.config, func)


class BaseScraper(object):
    """Base class for a web scraper"""

    def __init__(self):
        self.config = self.get_config()

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

    def get_config(self):
        """
        Return configuration structure
        Loads configuration file from source
        Parses to standard config representation
        """
        return Config(filename=self.config)

    def map_tree_to_config(self, tree, config):
        return config.map_to_config(tree)

    def scrape_article(self, abstract_url):
        """
        Scrape an html page which is an issue of the journal
        """
        tree, urls = self.get_tree(abstract_url)
        # Walk over config, populating from article tree
        article = self.map_tree_to_config(tree, self.config)
        # Add meta data
        article['source_urls'] = [uri for _, uri in urls]
        # Run cleaning methods over article data
        cleaned_article = self.clean(article)
        # Check that required data is returned
        self.valid(cleaned_article)
        return cleaned_article

    def check_value(self, value, key='', missing=[], **kwargs):
        if not value:
            missing.append(key)

    def valid(self, data):
        missing = []
        # Curry check_value with container for missing properties
        curried_check = functools.partial(self.check_value, missing=missing)
        # Walk over the acquired data to check a value is set for each property
        utils.walk_and_apply(data, curried_check)
        if missing:
            raise MinimumDataFailure(
                'Proprties: {}; have no value'.format(', '.join(missing))
                )
        return missing

    def clean(self, data):
        return data
