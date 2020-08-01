from flask import render_template
from hackerstash.lib.emails.base import Base


class MemberJoinedProject(Base):
    def __init__(self, email, payload):
        super().__init__(email, payload)

    @property
    def type(self):
        return 'MEMBER_JOINED_PROJECT'

    @property
    def body(self):
        return render_template('emails/member_joined_project.html', **self.payload)

    @property
    def text(self):
        return f'A new member has joined {self.payload["name"]}'

    @property
    def subject(self):
        return f'A new member has joined {self.payload["name"]}'