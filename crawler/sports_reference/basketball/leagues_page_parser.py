"""This parser processes the basketball-reference leagues page.
It returns a dict of `{(<season>, <league>): <url>}`, where 
`<season>` is in the yyyy-YY format (e.g. 2018-19 for the 2018 
to 2019 season) and `<league>` is 'NBA', 'ABA', or 'BAA'.

Key data is found using the CSS select statement

    `table#stats tr th[data-stat=season] a`

which contains the relative hrefs in the format `/leagues/NBA_2018.html`.
Some seasons have multiple active leagues, so a regex is used to extract 
the league data for differentiation.

Note that there may be a `tbody` tag between the `table` and `tr` 
which is something the browser adds in. It is not present in 
the source html.
"""

from bs4 import BeautifulSoup

from crawler.sports_reference.basketball.settings import BASE_URL

from urllib.parse import urljoin

import re

class LeaguesPageParser:

    SEASON_TAG = 'table#stats tr th[data-stat=season] a'
    RE_SEASON_URL = re.compile(r'/leagues/(NBA|ABA|BAA)_\d{4}.html')

    def __init__(self, html, parser='html.parser'):
        self.urls = dict()
        self.html = html
        self.parser = parser

    def handle_data(self):
        handler = BeautifulSoup(self.html, self.parser)
        season_links = handler.select(self.SEASON_TAG)
        for link in season_links:
            rel_href = link.get('href')
            try:
                league = self.RE_SEASON_URL.match(rel_href).group(1)
            except AttributeError:
                print("No relative href found. Is '{}'"
                      "in the correct format?".format(rel_href))
                pass
            else:
                key = (link.text.lower(), league)
                self.urls[key] = urljoin(BASE_URL, rel_href)

    def get_urls(self):
        if len(self.urls) == 0:
            self.handle_data()
        return self.urls
