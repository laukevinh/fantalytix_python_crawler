"""This parser processes the basketball-reference leagues page.
It returns an array of dictionaries, one per season, in the format

    {
        'league':'<league>',
        'start_year': <season_start_year>
        'end_year': <season_end_year>,
        'url': '<url>'
    }

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

from fantalytix_python_crawler.crawler.sports_reference.basketball\
    .settings import BASE_URL

from urllib.parse import urljoin

import re

from datetime import date

class LeaguesPageParser:

    SEASON_TAG = 'table#stats tr th[data-stat=season] a'
    RE_SEASON_URL = re.compile(r'/leagues/(NBA|ABA|BAA)_\d{4}.html')
    RE_SEASON_YEARS = re.compile(r'(\d{4})-\d{2}')

    def __init__(self, html, parser='html.parser'):
        self.data = []
        self.html = html
        self.parser = parser

    def season_years_text_to_date(self, text):
        """Converts seasons from text to date format.
        The output month and day is always Jan 1; only the year changes.
        End year is determined by start_year + 1, which correctly converts 
        the 1999-2000 season.
        """
        start_year = int(self.RE_SEASON_YEARS.match(text.lower()).group(1))
        end_year = start_year + 1
        return date(start_year, 1, 1), date(end_year, 1, 1)

    def handle_data(self):
        handler = BeautifulSoup(self.html, self.parser)
        season_links = handler.select(self.SEASON_TAG)
        for link in season_links:
            rel_href = link.get('href')
            try:
                league = self.RE_SEASON_URL.match(rel_href).group(1)
            except AttributeError:
                print("No relative href found. Is '{}' "
                      "in the correct format?".format(rel_href))
                pass
            try:
                start_year, end_year = self.season_years_text_to_date(
                    link.text.lower())
            except AttributeError:
                print("Start or end year not found. Is '{}' "
                      "in the correct format?".format(link.text.lower()))

            self.data.append({
                'league': league,
                'start_year': start_year,
                'end_year': end_year,
                'url': urljoin(BASE_URL, rel_href),
            })

    def get_data(self):
        if len(self.data) == 0:
            self.handle_data()
        return self.data
