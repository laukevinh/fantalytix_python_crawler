"""This parser processes the basketball-reference player directory
page. It returns a dict of `{'<letter>': '<url>'}`, where each url 
contains the players whose last name start with the same letter.

Key data are located under `ul.page_index > li > a`.

BeautifulSoup plus Python's html.parser are used for html parsing. 
BeautifulSoup plus lxml was tested as well but produces unexpected 
results. For example, the `ul.page_index > li > a` select statement 
produces only 1 element when 25 are expected.

Not all letters are used. Specifically no player has a last name 
that starts with 'X'.
"""

from bs4 import BeautifulSoup

from fantalytix_python_crawler.crawler.sports_reference.basketball\
    .settings import BASE_URL

from urllib.parse import urljoin

import re

class PlayersDirPageParser:

    LAST_NAME_LETTER_TAG = 'ul.page_index > li > a'
    RE_PLAYER_URL = re.compile(r'/players/[a-z]/')

    def __init__(self, html, parser='html.parser'):
        self.urls = dict()
        self.html = html
        self.parser = parser

    def handle_data(self):
        handler = BeautifulSoup(self.html, self.parser)
        last_name_letter_links = handler.select(self.LAST_NAME_LETTER_TAG)
        for link in last_name_letter_links:
            self.urls[link.text.lower()] = urljoin(BASE_URL, link.get('href'))
    
    def get_urls(self):
        if len(self.urls) == 0:
            self.handle_data()
        return self.urls
