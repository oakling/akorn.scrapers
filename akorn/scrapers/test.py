import unittest

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
