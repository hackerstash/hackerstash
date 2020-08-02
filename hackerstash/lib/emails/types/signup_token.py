from flask import render_template
from hackerstash.config import config
from hackerstash.lib.emails.base import Base


class SignupToken(Base):
    def __init__(self, email, payload):
        super().__init__(email, payload)

    @property
    def type(self):
        return 'SIGNUP_TOKEN'

    @property
    def body(self):
        return render_template('emails/signup_token.html', **self.payload, host=config['host'])

    @property
    def text(self):
        return f'Your sign up token is: {self.payload["token"]}'

    @property
    def subject(self):
        return 'Your sign up code for HackerStash'
