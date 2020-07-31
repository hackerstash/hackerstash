from flask import render_template
from hackerstash.lib.emails.base import Base


class RepliedToComment(Base):
    def __init__(self, email, payload):
        super().__init__(email, payload)

    @property
    def type(self):
        return 'REPLIED_TO_COMMENT'

    @property
    def body(self):
        return render_template('emails/replied_to_comment.html', **self.payload)

    @property
    def text(self):
        return 'Someone replied to your comment'

    @property
    def subject(self):
        return 'Someone replied to your comment'
