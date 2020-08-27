from flask import render_template
from hackerstash.config import config
from hackerstash.lib.emails.base import Base


class MentionedInComment(Base):
    def __init__(self, email: str, payload: dict) -> None:
        super().__init__(email, payload)

    @property
    def type(self) -> str:
        return 'MENTIONED_IN_COMMENT'

    @property
    def body(self) -> str:
        return render_template('emails/mentioned_in_comment.html', **self.payload, host=config['host'])

    @property
    def text(self) -> str:
        return 'You were mentioned in a comment'

    @property
    def subject(self) -> str:
        return 'You were mentioned in a comment'
