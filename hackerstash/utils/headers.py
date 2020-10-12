from flask import request, session
from hackerstash.utils.page import Page


class Headers:
    def __init__(self, response):
        self.path = request.path
        self.public = 'id' not in session
        self.response = response

        self.response.headers['server'] = 'teapot'
        self.response.headers['X-Content-Type-Options'] = 'nosniff'
        self.response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        self.response.headers['X-XSS-Protection'] = '1; mode=block'
        self.response.headers['Referrer-Policy'] = 'no-referrer-when-downgrade'
        self.response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

    @property
    def cache_mode(self):
        return 'public' if self.public else 'private'

    @property
    def one_year(self):
        return 'public, max-age=31536000'

    @property
    def one_hour(self):
        return f'{self.cache_mode}, max-age=3600'

    @property
    def twelve_seconds(self):
        return f'{self.cache_mode}, max-age=12'

    @property
    def five_seconds(self):
        return f'{self.cache_mode}, max-age=5'

    @property
    def private(self):
        return 'private, no-cache'

    def set_cache_control(self, value: str):
        self.response.headers['Cache-Control'] = value

    def set_cache_headers(self):
        page = Page(self.path)

        if page.static:
            self.set_cache_control(self.one_year)
        elif page.home or page.contact or page.rules or page.past_results:
            self.set_cache_control(self.one_hour)
        elif page.leaderboard:
            self.set_cache_control(self.twelve_seconds)
        elif page.users or page.projects or page.posts:
            self.set_cache_control(self.five_seconds)
        elif page.challenges or page.notifications or page.admin:
            self.set_cache_control(self.private)

        return self.response
