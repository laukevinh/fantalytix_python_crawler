"""This parser processes the basketball-reference season summary page. 
It returns an array of dictionaries containing active team names, their 
abbreviations and other information.

Getting team names and abbreviations from the each year's season summary 
page is the most accurate source. Other pages such as 
basketball-reference.com/teams/ list the name of all teams past and present, 
but only has the abbreviation for current teams.
"""

from bs4 import BeautifulSoup

from fantalytix_python_crawler.crawler.sports_reference.basketball\
    .settings import BASE_URL

from urllib.parse import urljoin

import re

from datetime import datetime, date, time

class SeasonSummaryPageParser:

    EAST_CONF_TABLE_ROWS = "#all_confs_standings_E table tbody tr"
    WEST_CONF_TABLE_ROWS = "#all_confs_standings_W table tbody tr"

    TEAM_NAME_URL_FIELD = "th[data-stat=team_name] a"

    RE_TEAM_SEASON_URL = re.compile(r'/teams/([A-Z]{3})/(\d{4}).html')

    def __init__(self, html, parser='html.parser'):
        self.data = []
        self.html = html
        self.parser = parser

    def get_abbreviation_and_year(self, rel_href):
        try:
            abbreviation, end_year = self.RE_TEAM_SEASON_URL.match(
                rel_href).groups()
        except AttributeError:
            print("Regex error: Abbreviation or year not found. Is "
                  "rel_href '{}' in the correct format?".format(rel_href))
            abbreviation, end_year = "", ""
        return {'abbreviation': abbreviation, 'end_year': end_year}

    def process_table_rows(self, team_rows):
        for row in team_rows:
            team_name_field = row.select(self.TEAM_NAME_URL_FIELD)[0]
            rel_href = team_name_field.get('href')
            data = self.get_abbreviation_and_year(rel_href)

            self.data.append({
                'team_name': team_name_field.text.lower(),
                'team_season_url': urljoin(BASE_URL, rel_href), 
                'abbreviation': data['abbreviation'],
                'end_year': data['end_year']
            })

    def handle_data(self):
        """The season summary table splits the team names into two tables."""
        handler = BeautifulSoup(self.html, self.parser)
        self.process_table_rows(handler.select(self.EAST_CONF_TABLE_ROWS))
        self.process_table_rows(handler.select(self.WEST_CONF_TABLE_ROWS))

    def get_data(self):
        if len(self.data) == 0:
            self.handle_data()
        return self.data
