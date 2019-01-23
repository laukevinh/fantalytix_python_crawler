"""This is a base parser class for inheriting. Contains basic helper 
functions such as getting team name abbreviations from urls.
"""

import re

class BasePageParser:

    RE_TEAM_SEASON_URL = re.compile(r'/teams'
                                    r'/(?P<abbreviation>[A-Z]{3})'
                                    r'/(?P<year>\d{4})'
                                    r'.html')

    def get_abbreviation_and_year_from_url(self, rel_href):
        try:
            abbreviation, end_year = self.RE_TEAM_SEASON_URL.match(
                rel_href).groups()
        except AttributeError:
            print("Regex error: Abbreviation or year not found. Is "
                  "rel_href '{}' in the correct format?".format(rel_href))
            abbreviation, end_year = "", ""
        return {'abbreviation': abbreviation, 'end_year': end_year}

    def get_abbreviation_from_url(self, rel_href):
        return self.get_abbreviation_and_year_from_url(rel_href)['abbreviation']
