import unittest
import lxml.html

import base

class NoConfigScraper(base.BaseScraper):
    def get_config_data_file(self):
        return None


class ValidBaseScraperTest(unittest.TestCase):
    all_props = {
            'title': 'fish',
            'author_names': 5,
            'abstract': 'horse',
            'date_published': 'test',
            'journal': None
        }

    def test_all_valid(self):
        scraper = NoConfigScraper()
        scraper.valid(self.all_props)
        # Check that base.MinimumDataFailure is not raised

    def test_one_missing(self):
        scraper = NoConfigScraper()
        one_missing = self.all_props
        del one_missing['title']
        with self.assertRaisesRegexp(base.MinimumDataFailure, 'title'):
            scraper.valid(one_missing)

    def test_empty_dict(self):
        scraper = NoConfigScraper()
        with self.assertRaises(base.MinimumDataFailure):
            scraper.valid({})


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

    def test_no_single(self):
        scraper = NoConfigScraper()
        out = scraper.get_meta('dc.not_there', self.source)
        self.assertEqual(out, None)

    def test_no_many(self):
        scraper = NoConfigScraper()
        out = scraper.get_meta_list('dc.not_there', self.source)
        self.assertEqual(out, None)

    def test_find_single_meta(self):
        scraper = NoConfigScraper()
        out = scraper.get_meta('dc.title', self.source)
        self.assertEqual(out, 'First')

    def test_find_many_meta(self):
        scraper = NoConfigScraper()
        out = scraper.get_meta_list('dc.title', self.source)
        self.assertEqual(out, ['First', 'Second', 'Third'])

    def test_find_wrong_case(self):
        scraper = NoConfigScraper()
        out = scraper.get_meta('DC.TItle', self.source)
        self.assertEqual(out, 'First')
