"""This parser processes the basketball-reference season schedules page. 
It returns an array of dictionaries, one per game day.
"""

from bs4 import BeautifulSoup

from fantalytix_python_crawler.crawler.sports_reference.basketball\
    .settings import BASE_URL

from urllib.parse import urljoin

from datetime import datetime, date, time

class SeasonSchedulePageParser:

    TABLE_SCHEDULE = "table#schedule"
    SEASON_SCHEDULE_TR = "table#schedule tbody tr"
    DATE_FIELD = "th[data-stat=date_game]"
    TIME_FIELD = "td[data-stat=game_start_time]"
    VISITOR_TEAM_FIELD = "td[data-stat=visitor_team_name]"
    VISITOR_PTS_FIELD = "td[data-stat=visitor_pts]"
    HOME_TEAM_FIELD = "td[data-stat=home_team_name]"
    HOME_PTS_FIELD = "td[data-stat=home_pts]"
    BOX_SCORE_FIELD = "td[data-stat=box_score_text]"
    OVERTIMES_FIELD = "td[data-stat=overtimes]"
    ATTENDANCE_FIELD = "td[data-stat=attendance]"

    COMMA            = ','
    GAME_DATE_FORMAT = '%a, %b %d, %Y'    #Tue, Oct 16, 2018
    GAME_TIME_FORMAT = '%I:%M%p'          #8:00p
    GAME_TIME_AM     = 'a'
    GAME_TIME_PM     = 'p'
    DATETIME_AM      = 'AM'
    DATETIME_PM      = 'PM'

    EMPTY_STR_AS_INT = -1

    def __init__(self, html, parser='html.parser'):
        self.data = []
        self.html = html
        self.parser = parser

    def text_to_int(self, text):
        """Games not yet played have an empty string for points, so 
        this parser translates these empty strings to the value defined by 
        EMPTY_STR_AS_INT.
        """
        try:
            return int(text.replace(self.COMMA, ''))
        except ValueError as err:
            return self.EMPTY_STR_AS_INT

    def get_abs_href_or_empty_str(self, html_field):
        """Returns the absolute url if available, otherwise empty string."""
        try:
            return urljoin(BASE_URL, html_field.get('href'))
        except AttributeError:
            return ""

    def game_date_text_to_date(self, text):
        """Converts text from the GAME_DATE_FORMAT to a python date object."""
        return datetime.strptime(text, self.GAME_DATE_FORMAT).date()

    def game_time_text_to_date(self, text):
        """Converts text from the GAME_TIME to a python time object."""
        if text[-1] is self.GAME_TIME_AM:
            text = text.replace(self.GAME_TIME_AM, self.DATETIME_AM)
        elif text[-1] is self.GAME_TIME_PM:
            text = text.replace(self.GAME_TIME_PM, self.DATETIME_PM)
        return datetime.strptime(text, self.GAME_TIME_FORMAT).time()

    def handle_data(self):
        handler = BeautifulSoup(self.html, self.parser)
        season_schedule_rows = handler.select(self.SEASON_SCHEDULE_TR)
        for row in season_schedule_rows:
            self.data.append({
                'game_date': self.game_date_text_to_date(
                    row.select(self.DATE_FIELD)[0].text),
                'game_start_time': self.game_time_text_to_date(
                    row.select(self.TIME_FIELD)[0].text.lower()),
                'visitor_team_name': row.select(self.VISITOR_TEAM_FIELD)[0]\
                    .text.lower(),
                'visitor_pts': self.text_to_int(
                    row.select(self.VISITOR_PTS_FIELD)[0].text),
                'home_team_name': row.select(self.HOME_TEAM_FIELD)[0]\
                    .text.lower(),
                'home_pts': self.text_to_int(
                    row.select(self.HOME_PTS_FIELD)[0].text),
                'box_score_text': self.get_abs_href_or_empty_str(row.select(
                    self.BOX_SCORE_FIELD)[0].a),
                'overtimes': row.select(self.OVERTIMES_FIELD)[0]\
                    .text.lower(),
                'attendance': self.text_to_int(
                    row.select(self.ATTENDANCE_FIELD)[0].text)
            })

    def get_data(self):
        if len(self.data) == 0:
            self.handle_data()
        return self.data
