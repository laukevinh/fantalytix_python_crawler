import unittest

from datetime import date

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

    def test_seasons_years_text_to_date(self):
        parser = leagues_page_parser.LeaguesPageParser("")
        self.assertEqual(parser.season_years_text_to_date('2015-16'),
            (date(2015, 1, 1), date(2016, 1, 1)))
        self.assertEqual(parser.season_years_text_to_date('1999-00'),
            (date(1999, 1, 1), date(2000, 1, 1)))

    def test_parser(self):
        with urlopen(urljoin(BASE_URL, LEAGUES_URL)) as resp:
            page = resp.read().decode('utf-8')
        parser = leagues_page_parser.LeaguesPageParser(page)

        seasons = [
            {
                'league': 'ABA',
                'start_year': date(1975, 1, 1),
                'end_year': date(1976, 1, 1),
                'url': 'https://www.basketball-reference.com/leagues/ABA_1976.html'
            },
            {
                'league': 'NBA',
                'start_year': date(2014, 1, 1),
                'end_year': date(2015, 1, 1),
                'url': 'https://www.basketball-reference.com/leagues/NBA_2015.html'
            },
            {
                'league': 'NBA',
                'start_year': date(2015, 1, 1),
                'end_year': date(2016, 1, 1),
                'url': 'https://www.basketball-reference.com/leagues/NBA_2016.html'
            },
            {
                'league': 'NBA',
                'start_year': date(2016, 1, 1),
                'end_year': date(2017, 1, 1),
                'url': 'https://www.basketball-reference.com/leagues/NBA_2017.html'
            }
        ]

        for season in seasons:
            self.assertTrue(season in parser.get_data())

        self.assertEqual(len(parser.get_data()), 82)

if __name__ == "__main__":
    unittest.main()
