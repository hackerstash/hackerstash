from flask import render_template
from hackerstash.config import config
from hackerstash.lib.emails.base import Base


class CommentedOnPost(Base):
    def __init__(self, email, payload):
        super().__init__(email, payload)

    @property
    def type(self):
        return 'COMMENTED_ON_POST'

    @property
    def body(self):
        return render_template('emails/commented_on_post.html', **self.payload, host=config['host'])

    @property
    def text(self):
        return 'Someone commented on your post'

    @property
    def subject(self):
        return 'Someone commented on your post'
