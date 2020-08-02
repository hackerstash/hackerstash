from flask import render_template
from hackerstash.config import config
from hackerstash.lib.emails.base import Base


class FollowerCreatedPost(Base):
    def __init__(self, email, payload):
        super().__init__(email, payload)

    @property
    def type(self):
        return 'FOLLOWER_CREATED_POST'

    @property
    def body(self):
        return render_template('emails/follower_created_post.html', **self.payload, host=config['host'])

    @property
    def text(self):
        return 'Someone you follow created a post'

    @property
    def subject(self):
        return 'Someone you follow created a post'
