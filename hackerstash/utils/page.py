from flask import url_for


class Page:
    def __init__(self, path):
        self.path = path

    @property
    def static(self):
        return self.path.startswith('/static') or self.path.endswith('.js') or self.path.endswith('.css')

    @property
    def home(self):
        return self.path == url_for('home.index')

    @property
    def contact(self):
        return self.path == url_for('contact.index')

    @property
    def rules(self):
        return self.path == url_for('rules.index')

    @property
    def leaderboard(self):
        return self.path == url_for('leaderboard.index')

    @property
    def posts(self):
        return self.path.startswith('/posts')

    @property
    def users(self):
        return self.path.startswith('/users')

    @property
    def projects(self):
        return self.path.startswith('/projects')

    @property
    def challenges(self):
        return self.path == url_for('challenges.index')

    @property
    def notifications(self):
        return self.path.startswith('/notifications')

    @property
    def admin(self):
        return self.path.startswith('/admin')

    @property
    def onboarding(self):
        return self.path.startswith('/onboarding')
