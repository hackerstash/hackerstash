from flask import render_template
from hackerstash.config import config
from hackerstash.lib.emails.base import Base


class VotedOnComment(Base):
    def __init__(self, email, payload):
        super().__init__(email, payload)

    @property
    def type(self):
        return 'VOTED_ON_COMMENT'

    @property
    def body(self):
        return render_template('emails/voted_on_comment.html', **self.payload, host=config['host'])

    @property
    def text(self):
        return f'Your comment was {self.payload["direction"].lower()}voted'

    @property
    def subject(self):
        return f'Your comment was {self.payload["direction"].lower()}voted'
