from flask import render_template
from hackerstash.config import config
from hackerstash.lib.emails.base import Base


class SignupToken(Base):
    def __init__(self, email: str, payload: dict) -> None:
        super().__init__(email, payload)

    @property
    def type(self) -> str:
        return 'SIGNUP_TOKEN'

    @property
    def body(self) -> str:
        return render_template('emails/signup_token.html', **self.payload, host=config['host'])

    @property
    def text(self) -> str:
        return f'Your sign up token is: {self.payload["token"]}'

    @property
    def subject(self) -> str:
        return 'Your sign up code for HackerStash'
