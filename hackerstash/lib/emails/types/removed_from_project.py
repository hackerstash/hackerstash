from flask import render_template
from hackerstash.config import config
from hackerstash.lib.emails.base import Base


class RemovedFromProject(Base):
    def __init__(self, email, payload):
        super().__init__(email, payload)

    @property
    def type(self):
        return 'REMOVED_FROM_PROJECT'

    @property
    def body(self):
        return render_template('emails/removed_from_project.html', **self.payload, host=config['host'])

    @property
    def text(self):
        return f'You have been removed from: {self.payload["member"].project.name}'

    @property
    def subject(self):
        return f'You\'ve been removed from {self.payload["member"].project.name}'
