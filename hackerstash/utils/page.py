from flask import url_for


class Page:
    def __init__(self, path) -> None:
        """
        Intialise an instance of the Page class
        :param path: str
        """
        self.path = path

    @property
    def static(self) -> bool:
        """
        Return if the path is a static file
        :return: bool
        """
        return self.path.startswith('/static') or self.path.endswith('.js') or self.path.endswith('.css')

    @property
    def home(self) -> bool:
        """
        Return if the path is for the home page
        :return: bool
        """
        return self.path == url_for('home.index')

    @property
    def contact(self) -> bool:
        """
        Return if the path is for the contact page
        :return: bool
        """
        return self.path == url_for('contact.index')

    @property
    def rules(self) -> bool:
        """
        Return if the path is for the rules page
        :return: bool
        """
        return self.path == url_for('rules.index')

    @property
    def leaderboard(self) -> bool:
        """
        Return if the path is for the leaderboard
        :return: bool
        """
        return self.path == url_for('leaderboard.index')

    @property
    def posts(self) -> bool:
        """
        Return if the path is for one of the posts pages
        :return: bool
        """
        return self.path.startswith('/posts')

    @property
    def users(self) -> bool:
        """
        Return if the path is for one of the users pages
        :return: bool
        """
        return self.path.startswith('/users')

    @property
    def projects(self) -> bool:
        """
        Return if the path is for one of the projects pages
        :return: bool
        """
        return self.path.startswith('/projects')

    @property
    def challenges(self) -> bool:
        """
        Return if the path is for the challenges page
        :return: bool
        """
        return self.path == url_for('challenges.index')

    @property
    def notifications(self) -> bool:
        """
        Return if the path is for one of the notifications pages
        :return: bool
        """
        return self.path.startswith('/notifications')

    @property
    def admin(self) -> bool:
        """
        Return if the path is for one of the admin pages
        :return: bool
        """
        return self.path.startswith('/admin')

    @property
    def onboarding(self) -> bool:
        """
        Return if the path is for one of the onboarding pages
        :return: bool
        """
        return self.path.startswith('/onboarding')
