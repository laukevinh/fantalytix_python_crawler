import unittest
from urllib.request import urlopen

from urllib.parse import urljoin

from crawler.sports_reference.basketball import leagues_page_parser
from crawler.sports_reference.basketball.settings import (
    BASE_URL, LEAGUES_URL)

class TestLeaguesPageParser(unittest.TestCase):

    def test_leagues_page_url(self):
        self.assertEqual(
            urljoin(BASE_URL, LEAGUES_URL), 
            'https://www.basketball-reference.com/leagues'
        )

    def test_parser(self):
        with urlopen(urljoin(BASE_URL, LEAGUES_URL)) as resp:
            page = resp.read().decode('utf-8')
        parser = leagues_page_parser.LeaguesPageParser(page)

        urls = {
            ('1975-76', 'ABA'): 'https://www.basketball-reference.com/leagues/ABA_1976.html',
            ('2014-15', 'NBA'): 'https://www.basketball-reference.com/leagues/NBA_2015.html',
            ('2015-16', 'NBA'): 'https://www.basketball-reference.com/leagues/NBA_2016.html',
            ('2016-17', 'NBA'): 'https://www.basketball-reference.com/leagues/NBA_2017.html',
            ('2017-18', 'NBA'): 'https://www.basketball-reference.com/leagues/NBA_2018.html',
        }

        for key in urls.keys():
            self.assertEqual(urls[key], parser.get_urls()[key])

        self.assertEqual(len(parser.get_urls()), 82)

if __name__ == "__main__":
    unittest.main()
