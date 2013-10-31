import unittest
import lxml.html

from akorn.scrapers import base
from akorn.scrapers import utils

class NoConfigScraper(base.BaseScraper):
    def get_config(self):
        return None


class ValidBaseScraperTest(unittest.TestCase):
    scraped = {
            'title': 'fish',
            'author_names': 5,
            'abstract': 'horse',
            'date_published': 'test'
        }

    def test_all_valid(self):
        scraper = NoConfigScraper()
        missing = scraper.valid(self.scraped)
        self.assertEqual(missing, [])

    def test_one_missing(self):
        scraper = NoConfigScraper()
        one_missing = self.scraped
        one_missing['title'] = None
        with self.assertRaisesRegexp(base.MinimumDataFailure, 'title'):
            scraper.valid(one_missing)

    def test_many_missing(self):
        scraper = NoConfigScraper()
        one_missing = self.scraped
        one_missing['abstract'] = None
        one_missing['title'] = None
        with self.assertRaisesRegexp(base.MinimumDataFailure, 'abstract, title'):
            scraper.valid(one_missing)

    def test_empty_dict(self):
        scraper = NoConfigScraper()
        missing = scraper.valid({})
        self.assertEqual(missing, [])


class MetaTagTest(unittest.TestCase):
    xml = """
    <html>
        <head>
            <meta name="dc.title" content="First" />
            <meta name="dc.title" content="Second" />
            <meta name="dc.title" content="Third" />
            <level2>
                <meta name="dc.title" content="Too deep" />
            </level2>
        </head>
        <meta name="dc.title" content="Outside head" />
    </html>
    """

    def setUp(self):
        self.source = lxml.html.fromstring(self.xml)
        self.config = base.Config()

    def test_no_single(self):
        lookup = {'type': 'metaTag', 'value': 'dc.not_there'}
        compiled_func = self.config.compile_meta_single(lookup)
        out = compiled_func(self.source)
        self.assertEqual(out, None)

    def test_no_many(self):
        lookup = {'type': 'metaTag', 'value': 'dc.not_there'}
        compiled_func = self.config.compile_meta_single(lookup)
        out = compiled_func(self.source)
        self.assertEqual(out, None)

    def test_find_single_meta(self):
        lookup = {'type': 'metaTag', 'value': 'dc.title'}
        compiled_func = self.config.compile_meta_single(lookup)
        out = compiled_func(self.source)
        self.assertEqual(out, 'First')

    def test_find_many_meta(self):
        lookup = {'type': 'metaList', 'value': 'dc.title'}
        compiled_func = self.config.compile_meta(lookup)
        out = compiled_func(self.source)
        self.assertEqual(out, ['First', 'Second', 'Third'])

    def test_find_wrong_case(self):
        lookup = {'type': 'metaTag', 'value': 'DC.TItle'}
        compiled_func = self.config.compile_meta_single(lookup)
        out = compiled_func(self.source)
        self.assertEqual(out, 'First')


class TestWalkAndApply(unittest.TestCase):
    given = {
        'fish': 'house',
        'top': {
                'middle': {
                        'bottom': 'hello!'
                },
                'another': 'dog'
            }
        }
    expected = {
        'fish': 'HOUSE',
        'top': {
                'middle': {
                    'bottom': 'HELLO!'
                },
                'another': 'DOG'
            }
        }

    def function(self, string, **kwargs):
        return str.upper(string)

    def test_walk_dict(self):
        out = utils.walk_and_apply(self.given, self.function)
        self.assertEqual(self.expected, out)
