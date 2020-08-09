from flask import render_template
from hackerstash.config import config
from hackerstash.lib.emails.base import Base


class RepliedToComment(Base):
    def __init__(self, email: str, payload: dict) -> None:
        super().__init__(email, payload)

    @property
    def type(self) -> str:
        return 'REPLIED_TO_COMMENT'

    @property
    def body(self) -> str:
        return render_template('emails/replied_to_comment.html', **self.payload, host=config['host'])

    @property
    def text(self) -> str:
        return 'Someone replied to your comment'

    @property
    def subject(self) -> str:
        return 'Someone replied to your comment'
