from flask import render_template
from hackerstash.config import config
from hackerstash.lib.emails.base import Base


class CommentedOnPost(Base):
    def __init__(self, email: str, payload: dict) -> None:
        super().__init__(email, payload)

    @property
    def type(self) -> str:
        return 'COMMENTED_ON_POST'

    @property
    def body(self) -> str:
        return render_template('emails/commented_on_post.html', **self.payload, host=config['host'])

    @property
    def text(self) -> str:
        return 'Someone commented on your post'

    @property
    def subject(self) -> str:
        return 'Someone commented on your post'
