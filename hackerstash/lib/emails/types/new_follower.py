from flask import render_template
from hackerstash.config import config
from hackerstash.lib.emails.base import Base


class NewFollower(Base):
    def __init__(self, email: str, payload: dict) -> None:
        super().__init__(email, payload)

    @property
    def type(self) -> str:
        return 'NEW_FOLLOWER'

    @property
    def body(self) -> str:
        return render_template('emails/new_follower.html', **self.payload, host=config['host'])

    @property
    def text(self) -> str:
        return 'You have a new follower'

    @property
    def subject(self) -> str:
        return 'You have a new follower'
