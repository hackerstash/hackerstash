from flask import render_template
from hackerstash.lib.emails.base import Base


class NewFollower(Base):
    def __init__(self, email, payload):
        super().__init__(email, payload)

    @property
    def type(self):
        return 'NEW_FOLLOWER'

    @property
    def body(self):
        return render_template('emails/new_follower.html', **self.payload)

    @property
    def text(self):
        return 'You have a new follower'

    @property
    def subject(self):
        return 'You have a new follower'
