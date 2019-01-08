import unittest

from datetime import date

from urllib.request import urlopen

from urllib.parse import urljoin

from fantalytix_python_crawler.crawler.sports_reference.basketball\
    .boxscore_page_parser import BoxscorePageParser
from fantalytix_python_crawler.crawler.sports_reference.basketball\
    .settings import (BASE_URL, BOXSCORE_URL)

class TestBoxscorePageParser(unittest.TestCase):

    def setUp(self):
        self.url_params = {
            'YYYYMMDD': date(2018, 10, 31).strftime('%Y%m%d'),
            'abbreviation': 'GSW'
        }

    def test_boxscore_page_url(self):
        self.assertEqual(
            urljoin(BASE_URL, BOXSCORE_URL.format(**self.url_params)),
            ('https://www.basketball-reference.com/boxscores'
             '/201810310GSW.html')
        )

    def test_parser(self):
        abs_url = urljoin(BASE_URL, BOXSCORE_URL.format(**self.url_params))
        with urlopen(abs_url) as resp:
            page = resp.read().decode('utf-8')
        parser = BoxscorePageParser(page)

        self.assertEqual(
            parser.get_data()['home_team']['basic'][0], 
            {
                'player': 'Kevin Durant',
                'mp': '40:09',
                'fg': '10',
                'fga': '17',
                'fg_pct': '.588',
                'fg3': '2',
                'fg3a': '3',
                'fg3_pct': '.667',
                'ft': '2',
                'fta': '3',
                'ft_pct': '.667',
                'orb': '0',
                'drb': '5',
                'trb': '5',
                'ast': '8',
                'stl': '2',
                'blk': '0',
                'tov': '2',
                'pf': '0',
                'pts': '24',
                'plus_minus': '+12',
            }
        )

        self.assertEqual(
            parser.get_data()['home_team']['advanced'][0], 
            {
                'player': 'Kevin Durant',
                'mp': '40:09',
                'ts_pct': '.655',
                'efg_pct': '.647',
                'fg3a_per_fga_pct': '.176',
                'fta_per_fga_pct': '.176',
                'orb_pct': '0.0',
                'drb_pct': '13.0',
                'trb_pct': '6.8',
                'ast_pct': '27.3',
                'stl_pct': '2.3',
                'blk_pct': '0.0',
                'tov_pct': '9.8',
                'usg_pct': '20.4',
                'off_rtg': '131',
                'def_rtg': '116',
            }
        )

        self.assertEqual(
            parser.get_data()['away_team']['basic'][1], 
            {
                'player': 'Anthony Davis',
                'mp': '41:17',
                'fg': '6',
                'fga': '16',
                'fg_pct': '.375',
                'fg3': '1',
                'fg3a': '4',
                'fg3_pct': '.250',
                'ft': '4',
                'fta': '5',
                'ft_pct': '.800',
                'orb': '3',
                'drb': '9',
                'trb': '12',
                'ast': '7',
                'stl': '0',
                'blk': '1',
                'tov': '2',
                'pf': '3',
                'pts': '17',
                'plus_minus': '-2',
            }
        )

        self.assertEqual(
            parser.get_data()['away_team']['advanced'][1], 
            {
                'player': 'Anthony Davis',
                'mp': '41:17',
                'ts_pct': '.467',
                'efg_pct': '.406',
                'fg3a_per_fga_pct': '.250',
                'fta_per_fga_pct': '.313',
                'orb_pct': '7.6',
                'drb_pct': '24.9',
                'trb_pct': '15.9',
                'ast_pct': '22.0',
                'stl_pct': '0.0',
                'blk_pct': '2.0',
                'tov_pct': '9.9',
                'usg_pct': '19.8',
                'off_rtg': '111',
                'def_rtg': '125',
            }
        )

        self.assertEqual(
            parser.get_data()['home_team']['basic'][11], 
            {
                'player': 'Quinn Cook',
                'did_not_play': 'Did Not Play'
            }
        )

        self.assertEqual(
            parser.get_data()['home_team']['advanced'][11], 
            {
                'player': 'Quinn Cook',
                'did_not_play': 'Did Not Play'
            }
        )

        self.assertEqual(
            parser.get_data()['away_team']['basic'][5], 
            {
                'player': 'Julius Randle',
                'mp': '22:52',
                'fg': '3',
                'fga': '6',
                'fg_pct': '.500',
                'fg3': '0',
                'fg3a': '0',
                'fg3_pct': '',
                'ft': '5',
                'fta': '6',
                'ft_pct': '.833',
                'orb': '3',
                'drb': '7',
                'trb': '10',
                'ast': '2',
                'stl': '0',
                'blk': '0',
                'tov': '4',
                'pf': '3',
                'pts': '11',
                'plus_minus': '-23',
            }
        )

if __name__ == "__main__":
    unittest.main()
