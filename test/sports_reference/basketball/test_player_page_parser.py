import unittest

from datetime import date

from urllib.request import urlopen

from urllib.parse import urljoin

from fantalytix_python_crawler.crawler.sports_reference.basketball\
    .player_page_parser import PlayerPageParser
from fantalytix_python_crawler.crawler.sports_reference.basketball\
    .settings import (BASE_URL, PLAYER_URL)

class TestPlayerPageParser(unittest.TestCase):

    def test_player_page_url(self):
        self.assertEqual(
            urljoin(BASE_URL, PLAYER_URL), 
            'https://www.basketball-reference.com/players'
        )

    def test_birthday_text_to_date(self):
        parser = PlayerPageParser("")
        self.assertEqual(parser.birthday_text_to_date('1999-07-20'),
            date(1999, 7, 20))
        self.assertEqual(parser.birthday_text_to_date('1994-03-16'),
            date(1994, 3, 16))

    def test_weight_text_to_int(self):
        parser = PlayerPageParser("")
        self.assertEqual(parser.weight_text_to_int('205lb'), 205)
        self.assertEqual(parser.weight_text_to_int('100kg'), 220)

    def test_parser(self):
        player_url = ('https://www.basketball-reference.com/players/'
                      's/simmobe01.html')
        player = {
            'name': 'Ben Simmons',
            'height': '6-10',
            'weight': 230,
            'birthday': date(1996, 7, 20),
            'birthplace': '\n    in\xa0Melbourne,\xa0Australia',
            'nationality': 'au'
        }

        with urlopen(player_url) as resp:
            page = resp.read().decode('utf-8')
        parser = PlayerPageParser(page)

        self.assertEqual(player, parser.get_data())

if __name__ == "__main__":
    unittest.main()
