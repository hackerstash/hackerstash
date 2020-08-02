from flask import render_template
from hackerstash.config import config
from hackerstash.lib.emails.base import Base


class VotedOnPost(Base):
    def __init__(self, email, payload):
        super().__init__(email, payload)

    @property
    def type(self):
        return 'VOTED_ON_POST'

    @property
    def body(self):
        return render_template('emails/voted_on_post.html', **self.payload, host=config['host'])

    @property
    def text(self):
        return f'Your post was {self.payload["direction"].lower()}voted'

    @property
    def subject(self):
        return f'Your post was {self.payload["direction"].lower()}voted'
