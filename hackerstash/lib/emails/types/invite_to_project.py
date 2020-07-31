from flask import render_template
from hackerstash.lib.emails.base import Base


class InviteToProject(Base):
    def __init__(self, email, payload):
        super().__init__(email, payload)

    @property
    def type(self):
        return 'INVITE_TO_PROJECT'

    @property
    def body(self):
        return render_template('emails/invite_to_project.html', **self.payload)

    @property
    def text(self):
        return f'Click this link to accept your invite: {self.payload["link"]}'

    @property
    def subject(self):
        return 'You\'ve been invited to join a project on HackerStash'
