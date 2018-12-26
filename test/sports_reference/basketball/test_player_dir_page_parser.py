import unittest
from urllib.request import urlopen

from urllib.parse import urljoin

from fantalytix_python_crawler.crawler.sports_reference.basketball\
    .player_dir_page_parser import PlayersDirPageParser
from fantalytix_python_crawler.crawler.sports_reference.basketball\
    .settings import (BASE_URL, PLAYER_URL)


class TestPlayerDirPageParser(unittest.TestCase):

    def test_player_page_url(self):
        self.assertEqual(
            urljoin(BASE_URL, PLAYER_URL), 
            'https://www.basketball-reference.com/players'
        )

    def test_parser(self):
        with urlopen(urljoin(BASE_URL, PLAYER_URL)) as resp:
            page = resp.read().decode('utf-8')
        parser = PlayersDirPageParser(str(page))

        urls = {
            'a': 'https://www.basketball-reference.com/players/a/',
            'b': 'https://www.basketball-reference.com/players/b/',
            'c': 'https://www.basketball-reference.com/players/c/',
            'd': 'https://www.basketball-reference.com/players/d/',
            'e': 'https://www.basketball-reference.com/players/e/',
            'f': 'https://www.basketball-reference.com/players/f/',
            'g': 'https://www.basketball-reference.com/players/g/',
            'h': 'https://www.basketball-reference.com/players/h/',
            'i': 'https://www.basketball-reference.com/players/i/',
            'j': 'https://www.basketball-reference.com/players/j/',
            'k': 'https://www.basketball-reference.com/players/k/',
            'l': 'https://www.basketball-reference.com/players/l/',
            'm': 'https://www.basketball-reference.com/players/m/',
            'n': 'https://www.basketball-reference.com/players/n/',
            'o': 'https://www.basketball-reference.com/players/o/',
            'p': 'https://www.basketball-reference.com/players/p/',
            'q': 'https://www.basketball-reference.com/players/q/',
            'r': 'https://www.basketball-reference.com/players/r/',
            's': 'https://www.basketball-reference.com/players/s/',
            't': 'https://www.basketball-reference.com/players/t/',
            'u': 'https://www.basketball-reference.com/players/u/',
            'v': 'https://www.basketball-reference.com/players/v/',
            'w': 'https://www.basketball-reference.com/players/w/',
            'y': 'https://www.basketball-reference.com/players/y/',
            'z': 'https://www.basketball-reference.com/players/z/'
        }

        self.assertEqual(urls['a'], parser.get_urls()['a'])
        self.assertEqual(urls['z'], parser.get_urls()['z'])
        self.assertEqual(len(parser.get_urls()), 25)

if __name__ == "__main__":
    unittest.main()
