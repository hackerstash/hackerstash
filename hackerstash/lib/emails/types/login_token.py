from flask import render_template
from hackerstash.config import config
from hackerstash.lib.emails.base import Base


class LoginToken(Base):
    def __init__(self, email: str, payload: dict) -> None:
        super().__init__(email, payload)

    @property
    def type(self) -> str:
        return 'LOGIN_TOKEN'

    @property
    def body(self) -> str:
        return render_template('emails/login_token.html', **self.payload, host=config['host'])

    @property
    def text(self) -> str:
        return f'Your log in token is: {self.payload["token"]}'

    @property
    def subject(self) -> str:
        return 'Your log in code for HackerStash'
