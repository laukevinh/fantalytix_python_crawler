import unittest

from datetime import date, time

from urllib.request import urlopen

from urllib.parse import urljoin

from fantalytix_python_crawler.crawler.sports_reference.basketball\
    .season_schedule_page_parser import SeasonSchedulePageParser
from fantalytix_python_crawler.crawler.sports_reference.basketball\
    .settings import (BASE_URL, SEASON_SCHEDULE_URL)

class TestSeasonSchedulePageParser(unittest.TestCase):

    def setUp(self):
        self.url_params = {'league':'NBA', 'end_year':'2019', 'month':'october'} 

    def test_season_schedule_page_url(self):
        self.assertEqual(
            urljoin(BASE_URL, SEASON_SCHEDULE_URL.format(**self.url_params)),
            ('https://www.basketball-reference.com/leagues/'
             'NBA_2019_games-october.html')
        )

    def test_empty_text_to_int(self):
        """Games not yet played have an empty string for points. Test that 
        this parser translates these empty strings as a set value, originally 
        -1.
        """
        parser = SeasonSchedulePageParser("")
        self.assertEqual(parser.text_to_int(""), parser.EMPTY_STR_AS_INT)

    def test_get_abs_href_or_empty_str(self):
        """Games not yet played have an empty string for boxscore. Test that 
        this parser handles those correctly.
        """
        parser = SeasonSchedulePageParser("")
        self.assertEqual(parser.get_abs_href_or_empty_str(""), "")

    def test_parser(self):
        abs_url=urljoin(BASE_URL, SEASON_SCHEDULE_URL.format(**self.url_params))
        with urlopen(abs_url) as resp:
            page = resp.read().decode('utf-8')
        parser = SeasonSchedulePageParser(page)

        season_schedules = [
            {
                'game_date': date(2018, 10, 16),
                'game_start_time': time(20, 0),
                'visitor_team_name': 'philadelphia 76ers',
                'visitor_pts': 87,
                'home_team_name': 'boston celtics',
                'home_pts': 105,
                'box_score_text': ('https://www.basketball-reference.com/'
                                   'boxscores/201810160BOS.html'),
                'overtimes': '',
                'attendance': 18624,
                'type': parser.REGULAR_GAME
            },
        ]

        for season_schedule in season_schedules:
            self.assertTrue(season_schedule in parser.get_data())

        self.assertEqual(len(parser.get_data()), 110)

if __name__ == "__main__":
    unittest.main()
