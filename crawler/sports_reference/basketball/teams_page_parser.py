"""This parser processes the basketball-reference teams page.
It returns a list of dictionaries, one per team, in the format

    {
        'name': '<name>',
        'abbreviation': '<abbreviation>',
        'status': '<status>',
        'url': '<url>'
    }

Key data is found using the CSS select statement

    `#all_teams_active tr.full_table th[data-stat=franch_name] a`

which contains the relative hrefs in the format `/teams/ATL/`.
"""

from bs4 import BeautifulSoup

from fantalytix_python_crawler.crawler.sports_reference.basketball\
    .settings import BASE_URL

from urllib.parse import urljoin

import re

class TeamsPageParser:

    TEAM_TAG = '#all_teams_active tr.full_table th[data-stat=franch_name] a'
    RE_TEAM_URL = re.compile(r'/teams/([A-Z]{3})/')

    def __init__(self, html, parser='html.parser'):
        self.data = []
        self.html = html
        self.parser = parser

    def handle_data(self):
        handler = BeautifulSoup(self.html, self.parser)
        team_links = handler.select(self.TEAM_TAG)
        for link in team_links:
            rel_href = link.get('href')
            try:
                abbreviation = self.RE_TEAM_URL.match(rel_href).group(1)
            except AttributeError:
                print("No relative href found. Is '{}'"
                      "in the correct format?".format(rel_href))
                pass
            else:
                self.data.append({
                    'name': link.text.lower(),
                    'abbreviation': abbreviation,
                    'status': 'active',
                    'url': urljoin(BASE_URL, rel_href)
                })

    def get_data(self):
        if len(self.data) == 0:
            self.handle_data()
        return self.data
