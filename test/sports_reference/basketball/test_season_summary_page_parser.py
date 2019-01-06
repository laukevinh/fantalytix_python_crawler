import unittest

from datetime import date, time

from urllib.request import urlopen

from urllib.parse import urljoin

from fantalytix_python_crawler.crawler.sports_reference.basketball\
    .season_summary_page_parser import SeasonSummaryPageParser
from fantalytix_python_crawler.crawler.sports_reference.basketball\
    .settings import (BASE_URL, SEASON_SUMMARY_URL)

class TestSeasonSummaryPageParser(unittest.TestCase):

    def setUp(self):
        self.url_params = {'league':'NBA', 'end_year':'2019'} 

    def test_season_summary_page_url(self):
        self.assertEqual(
            urljoin(BASE_URL, SEASON_SUMMARY_URL.format(**self.url_params)),
            ('https://www.basketball-reference.com/leagues/NBA_2019.html')
        )

    def test_parser(self):
        abs_url=urljoin(BASE_URL, SEASON_SUMMARY_URL.format(**self.url_params))
        with urlopen(abs_url) as resp:
            page = resp.read().decode('utf-8')
        parser = SeasonSummaryPageParser(page)

        teams = [
            {
                'team_name': 'milwaukee bucks',
                'team_season_url': ('https://www.basketball-reference.com/'
                                    'teams/MIL/2019.html'),
                'abbreviation': 'MIL',
                'end_year': '2019'
            },
            {
                'team_name': 'phoenix suns',
                'team_season_url': ('https://www.basketball-reference.com/'
                                    'teams/PHO/2019.html'),
                'abbreviation': 'PHO',
                'end_year': '2019'
            },
        ]

        for team in teams:
            self.assertTrue(team in parser.get_data())

        self.assertEqual(len(parser.get_data()), 30)

    def test_get_abbreviation_and_year(self):
        parser = SeasonSummaryPageParser("")

        self.assertEqual({'abbreviation': 'PHO', 'end_year': '2019'},
            parser.get_abbreviation_and_year('/teams/PHO/2019.html'))
        self.assertEqual({'abbreviation': '', 'end_year': ''},
            parser.get_abbreviation_and_year('/teams/PHO/201920.html'))
        self.assertEqual({'abbreviation': '', 'end_year': ''},
            parser.get_abbreviation_and_year('/teams/BADABBR/2019.html'))

if __name__ == "__main__":
    unittest.main()
