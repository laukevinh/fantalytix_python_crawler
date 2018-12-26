import unittest
from urllib.request import urlopen

from urllib.parse import urljoin

from fantalytix_python_crawler.crawler.sports_reference.basketball\
    .teams_page_parser import TeamsPageParser
from fantalytix_python_crawler.crawler.sports_reference.basketball\
    .settings import (BASE_URL, TEAMS_URL)


class TestTeamsPageParser(unittest.TestCase):

    def test_teams_page_url(self):
        self.assertEqual(
            urljoin(BASE_URL, TEAMS_URL), 
            'https://www.basketball-reference.com/teams'
        )

    def test_parser(self):
        with urlopen(urljoin(BASE_URL, TEAMS_URL)) as resp:
            page = resp.read().decode('utf-8')
        parser = TeamsPageParser(page)

        teams = [
            {
                'name': 'atlanta hawks',
                'abbreviation': 'ATL',
                'status': 'active',
                'url': 'https://www.basketball-reference.com/teams/ATL/'
            },
            {
                'name': 'golden state warriors',
                'abbreviation': 'GSW',
                'status': 'active',
                'url': 'https://www.basketball-reference.com/teams/GSW/'
            },
            {
                'name': 'phoenix suns',
                'abbreviation': 'PHO',
                'status': 'active',
                'url': 'https://www.basketball-reference.com/teams/PHO/'
            },
            {
                'name': 'washington wizards',
                'abbreviation': 'WAS',
                'status': 'active',
                'url': 'https://www.basketball-reference.com/teams/WAS/'
            }
        ]

        for team in teams:
            self.assertTrue(team in parser.get_data())

        self.assertEqual(len(parser.get_data()), 30)

if __name__ == "__main__":
    unittest.main()
