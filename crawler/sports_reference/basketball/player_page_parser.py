"""This parser processes a single basketball-reference player page.
It returns the key player information as a dictionary, in the format

    {
        'name': '<name>',
        'height': <height>,
        'weight': <weight>,
        'birthday': <birthdate>,
        'birthplace': '<birthplace>',
        'nationality': '<nationality>'
    }
"""

from bs4 import BeautifulSoup

import re

from datetime import datetime

class PlayerPageParser:

    DIV_PLAYER_META   = 'div#meta'
    NAME_FIELD        = ' '.join([DIV_PLAYER_META, 'h1[itemprop=name]'])
    HEIGHT_FIELD      = ' '.join([DIV_PLAYER_META, 'span[itemprop=height]'])
    WEIGHT_FIELD      = ' '.join([DIV_PLAYER_META, 'span[itemprop=weight]'])
    BIRTHDAY_FIELD    = ' '.join([DIV_PLAYER_META, 'span[itemprop=birthDate]'])
    BIRTHDAY_ATTR     = 'data-birth'
    BIRTHPLACE_FIELD  = ' '.join([DIV_PLAYER_META, 'span[itemprop=birthPlace]'])
    NATIONALITY_FIELD = ' '.join([DIV_PLAYER_META, 'span.f-i'])

    DATE_FORMAT       = '%Y-%m-%d'

    RE_WEIGHT         = re.compile(r'(\d+)(lb|kg)')
    LBtoKG            = 2.20462
    LB                = 'lb'
    KG                = 'kg'

    def __init__(self, html, parser='html.parser'):
        self.data = dict() 
        self.html = html
        self.parser = parser

    def birthday_text_to_date(self, text):
        """Converts text from the DATE_FORMAT to a python date object."""
        return datetime.strptime(text, self.DATE_FORMAT).date()

    def weight_text_to_int(self, text):
        try:
            weight, unit = self.RE_WEIGHT.match(text).groups()
        except AttributeError:
            print("Weight or unit of measure not found. Is '{}' "
                  "in the correct format?".format(text))
            return None
        else:
            if unit in self.LB:
                return int(weight)
            if unit in self.KG:
                return round(int(weight) * self.LBtoKG)

    def handle_data(self):
        """Each bs4 CSS select query returns a list, so data must be retrieved 
        by accessing the first entry. Birthday is a more complicated field that
        is best crawled by accessing the 'data-birth' attribute.
        """
        handler = BeautifulSoup(self.html, self.parser)

        self.data['name'] = handler.select(self.NAME_FIELD)[0].text
        self.data['height'] = handler.select(self.HEIGHT_FIELD)[0].text
        self.data['weight'] = self.weight_text_to_int(
            handler.select(self.WEIGHT_FIELD)[0].text)
        self.data['birthday'] = self.birthday_text_to_date(
            handler.select(self.BIRTHDAY_FIELD)[0][self.BIRTHDAY_ATTR])
        self.data['birthplace'] = handler.select(self.BIRTHPLACE_FIELD)[0].text
        self.data['nationality'] = handler.select(
            self.NATIONALITY_FIELD)[0].text

    def get_data(self):
        if len(self.data) == 0:
            self.handle_data()
        return self.data
