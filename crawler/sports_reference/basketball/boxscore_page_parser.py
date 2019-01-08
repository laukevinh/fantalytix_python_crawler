"""This parser processes a basketball-reference boxscore page.
It returns a dictionary containing the basic and advanced scores 
for both the home and away teams.

    {
        'home_team': { 
            'basic': [{<player_data>}, ... ],
            'advanced': [{<player_data>}, ...]
        },
        'away_team': {
            'basic': [{<player_data>}, ... ],
            'advanced': [{<player_data>}, ...]
        }
    }
"""

from bs4 import BeautifulSoup

from fantalytix_python_crawler.crawler.sports_reference.basketball\
    .settings import BASE_URL

from .base_page_parser import BasePageParser

from urllib.parse import urljoin

import re

from datetime import date

class BoxscorePageParser(BasePageParser):

    DIV_SCOREBOX = "div.scorebox"
    TEAM_NAME_FIELD = "a[itemprop=name]"
    AWAY_TEAM_INDEX = 0
    HOME_TEAM_INDEX = 1

    DID_NOT_PLAY_FIELD = "td[data-stat=reason]"
    PLAYER_FIELD = "th[data-stat=player]"
    MP_FIELD = "td[data-stat=mp]"
    NO_MINUTES = "00:00"

    TABLE_BASIC_BOX_SCORE = "table#box_{abbreviation}_basic"
    FG_FIELD = "td[data-stat=fg]"
    FGA_FIELD = "td[data-stat=fga]"
    FG_PCT_FIELD = "td[data-stat=fg_pct]"
    FG3_FIELD = "td[data-stat=fg3]"
    FG3A_FIELD = "td[data-stat=fg3a]"
    FG3_PCT_FIELD = "td[data-stat=fg3_pct]"
    FT_FIELD = "td[data-stat=ft]"
    FTA_FIELD = "td[data-stat=fta]"
    FT_PCT_FIELD = "td[data-stat=ft_pct]"
    ORB_FIELD = "td[data-stat=orb]"
    DRB_FIELD = "td[data-stat=drb]"
    TRB_FIELD = "td[data-stat=trb]"
    AST_FIELD = "td[data-stat=ast]"
    STL_FIELD = "td[data-stat=stl]"
    BLK_FIELD = "td[data-stat=blk]"
    TOV_FIELD = "td[data-stat=tov]"
    PF_FIELD = "td[data-stat=pf]"
    PTS_FIELD = "td[data-stat=pts]"
    PLUS_MINUS_FIELD = "td[data-stat=plus_minus]"

    TABLE_ADVANCED_BOX_SCORE = "table#box_{abbreviation}_advanced"
    TS_PCT_FIELD = "td[data-stat=ts_pct]"
    EFG_PCT_FIELD = "td[data-stat=efg_pct]"
    FG3A_PER_FGA_PCT_FIELD = "td[data-stat=fg3a_per_fga_pct]"
    FTA_PER_FGA_PCT_FIELD = "td[data-stat=fta_per_fga_pct]"
    ORB_PCT_FIELD = "td[data-stat=orb_pct]"
    DRB_PCT_FIELD = "td[data-stat=drb_pct]"
    TRB_PCT_FIELD = "td[data-stat=trb_pct]"
    AST_PCT_FIELD = "td[data-stat=ast_pct]"
    STL_PCT_FIELD = "td[data-stat=stl_pct]"
    BLK_PCT_FIELD = "td[data-stat=blk_pct]"
    TOV_PCT_FIELD = "td[data-stat=tov_pct]"
    USG_PCT_FIELD = "td[data-stat=usg_pct]"
    OFF_RTG_FIELD = "td[data-stat=off_rtg]"
    DEF_RTG_FIELD = "td[data-stat=def_rtg]"

    def __init__(self, html, parser='html.parser'):
        self.data = {
            'home_team': {'basic': [], 'advanced': []},
            'away_team': {'basic': [], 'advanced': []}
        }
        self.html = html
        self.parser = parser

    def get_team_season_url_fields(self, handler):
        url_fields = handler.select(" ".join([self.DIV_SCOREBOX, 
            self.TEAM_NAME_FIELD]))
        return url_fields[self.HOME_TEAM_INDEX], url_fields[self.AWAY_TEAM_INDEX]

    def process_basic_box_table(self, handler, abbreviation, data):
        table = handler.select(self.TABLE_BASIC_BOX_SCORE.format(
            abbreviation=abbreviation))[0]
        for row in table.tbody.find_all('tr'):
            if row.get('class') is None:
                if len(row.select(self.DID_NOT_PLAY_FIELD)) == 0:
                    data.append({
                        'player': row.select(self.PLAYER_FIELD)[0].text,
                        'mp': row.select(self.MP_FIELD)[0].text,
                        'fg': row.select(self.FG_FIELD)[0].text,
                        'fga': row.select(self.FGA_FIELD)[0].text,
                        'fg_pct': row.select(self.FG_PCT_FIELD)[0].text,
                        'fg3': row.select(self.FG3_FIELD)[0].text,
                        'fg3a': row.select(self.FG3A_FIELD)[0].text,
                        'fg3_pct': row.select(self.FG3_PCT_FIELD)[0].text,
                        'ft': row.select(self.FT_FIELD)[0].text,
                        'fta': row.select(self.FTA_FIELD)[0].text,
                        'ft_pct': row.select(self.FT_PCT_FIELD)[0].text,
                        'orb': row.select(self.ORB_FIELD)[0].text,
                        'drb': row.select(self.DRB_FIELD)[0].text,
                        'trb': row.select(self.TRB_FIELD)[0].text,
                        'ast': row.select(self.AST_FIELD)[0].text,
                        'stl': row.select(self.STL_FIELD)[0].text,
                        'blk': row.select(self.BLK_FIELD)[0].text,
                        'tov': row.select(self.TOV_FIELD)[0].text,
                        'pf': row.select(self.PF_FIELD)[0].text,
                        'pts': row.select(self.PTS_FIELD)[0].text,
                        'plus_minus': row.select(self.PLUS_MINUS_FIELD)[0].text,
                    })
                else:
                    data.append({
                        'player': row.select(self.PLAYER_FIELD)[0].text,
                        'did_not_play': row.select(self.DID_NOT_PLAY_FIELD)[0].text
                    })

    def process_advanced_box_table(self, handler, abbreviation, data):
        table = handler.select(self.TABLE_ADVANCED_BOX_SCORE.format(
            abbreviation=abbreviation))[0]
        for row in table.tbody.find_all('tr'):
            if row.get('class') is None:
                if len(row.select(self.DID_NOT_PLAY_FIELD)) == 0:
                    data.append({
                        'player': row.select(self.PLAYER_FIELD)[0].text,
                        'mp': row.select(self.MP_FIELD)[0].text,
                        'ts_pct': row.select(self.TS_PCT_FIELD)[0].text,
                        'efg_pct': row.select(self.EFG_PCT_FIELD)[0].text,
                        'fg3a_per_fga_pct': row.select(self.FG3A_PER_FGA_PCT_FIELD)[0].text,
                        'fta_per_fga_pct': row.select(self.FTA_PER_FGA_PCT_FIELD)[0].text,
                        'orb_pct': row.select(self.ORB_PCT_FIELD)[0].text,
                        'drb_pct': row.select(self.DRB_PCT_FIELD)[0].text,
                        'trb_pct': row.select(self.TRB_PCT_FIELD)[0].text,
                        'ast_pct': row.select(self.AST_PCT_FIELD)[0].text,
                        'stl_pct': row.select(self.STL_PCT_FIELD)[0].text,
                        'blk_pct': row.select(self.BLK_PCT_FIELD)[0].text,
                        'tov_pct': row.select(self.TOV_PCT_FIELD)[0].text,
                        'usg_pct': row.select(self.USG_PCT_FIELD)[0].text,
                        'off_rtg': row.select(self.OFF_RTG_FIELD)[0].text,
                        'def_rtg': row.select(self.DEF_RTG_FIELD)[0].text
                    })
                else:
                    data.append({
                        'player': row.select(self.PLAYER_FIELD)[0].text,
                        'did_not_play': row.select(self.DID_NOT_PLAY_FIELD)[0].text
                    })

    def handle_data(self):
        handler = BeautifulSoup(self.html, self.parser)
        home_team_field, away_team_field = self.get_team_season_url_fields(handler)
        home_team = self.get_abbreviation_from_url(home_team_field.get('href'))
        away_team = self.get_abbreviation_from_url(away_team_field.get('href'))

        self.process_basic_box_table(handler, home_team.lower(), 
            self.data['home_team']['basic'])
        self.process_basic_box_table(handler, away_team.lower(), 
            self.data['away_team']['basic'])
        self.process_advanced_box_table(handler, home_team.lower(),
            self.data['home_team']['advanced'])
        self.process_advanced_box_table(handler, away_team.lower(),
            self.data['away_team']['advanced'])

    def get_data(self):
        if (len(self.data['home_team']['basic']) == 0 
            or len(self.data['away_team']['basic']) == 0):
            # refresh if either home or away team basic stats are empty
            self.handle_data()
        return self.data
