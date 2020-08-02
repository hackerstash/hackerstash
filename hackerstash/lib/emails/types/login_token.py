from flask import render_template
from hackerstash.config import config
from hackerstash.lib.emails.base import Base


class LoginToken(Base):
    def __init__(self, email, payload):
        super().__init__(email, payload)

    @property
    def type(self):
        return 'LOGIN_TOKEN'

    @property
    def body(self):
        return render_template('emails/login_token.html', **self.payload, host=config['host'])

    @property
    def text(self):
        return f'Your log in token is: {self.payload["token"]}'

    @property
    def subject(self):
        return 'Your log in code for HackerStash'
