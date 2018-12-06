"""This parser processes the basketball-reference player directory
page. It can return a list of urls that each contain the players 
whose last name start with the same letter. It also returns the 
list of letters.

Not all letters are used. Specifically no player has a last name 
that starts with 'X'.

The DOM structure has <a> tags that point to the "players whose
last name starts with <letter>" page. It also has <a> tags that
point to a handful of popular players within the same section.

The former reside in `li a` tags while the latter reside in
`li div a` tags.
"""

from html.parser import HTMLParser

from crawler.sports_reference.basketball.settings import BASE_URL

from urllib.parse import urljoin

class PlayersDirPageParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.urls = dict()
        self.keys = []
        self.vals = []
        self.in_recording_zone = False
        self.begin_recording = False
        self.recording = False

    def handle_starttag(self, tag, attrs):
        if tag == 'ul' and ('class', 'page_index') in attrs:
            self.in_recording_zone = True
            self.begin_recording = True
            return
        if self.in_recording_zone:
            if tag == 'div':
                self.begin_recording = False
                return
            if tag == 'a' and self.begin_recording:
                self.recording = True
                for name, value in attrs:
                    if name == 'href':
                        self.vals.append(value)
                return

    def handle_endtag(self, tag):
        if self.in_recording_zone:
            if tag == 'ul':
                self.in_recording_zone = False
                self.begin_recording = False
                return
            if tag == 'div':
                self.begin_recording = True
                return
            if tag == 'a':
                self.recording = False
                return

    def handle_data(self, data):
        if self.recording:
            self.keys.append(data)
            return
    
    def update_urls(self):
        for key, val in zip(self.keys, self.vals):
            self.urls[key.lower()] = urljoin(BASE_URL, val)

    def get_urls(self):
        if len(self.urls) == 0:
            self.update_urls()
        return self.urls
