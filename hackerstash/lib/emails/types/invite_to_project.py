from flask import render_template
from hackerstash.config import config
from hackerstash.lib.emails.base import Base


class InviteToProject(Base):
    def __init__(self, email: str, payload: dict) -> None:
        super().__init__(email, payload)

    @property
    def type(self) -> str:
        return 'INVITE_TO_PROJECT'

    @property
    def body(self) -> str:
        return render_template('emails/invite_to_project.html', **self.payload, host=config['host'])

    @property
    def text(self) -> str:
        return f'Click this link to accept your invite: {self.payload["invite"].link}'

    @property
    def subject(self) -> str:
        return 'You\'ve been invited to join a project on HackerStash'
