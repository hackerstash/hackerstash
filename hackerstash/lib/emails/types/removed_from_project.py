from flask import render_template
from hackerstash.config import config
from hackerstash.lib.emails.base import Base


class RemovedFromProject(Base):
    def __init__(self, email: str, payload: dict) -> None:
        super().__init__(email, payload)

    @property
    def type(self) -> str:
        return 'REMOVED_FROM_PROJECT'

    @property
    def body(self) -> str:
        return render_template('emails/removed_from_project.html', **self.payload, host=config['host'])

    @property
    def text(self) -> str:
        return f'You have been removed from: {self.payload["member"].project.name}'

    @property
    def subject(self) -> str:
        return f'You\'ve been removed from {self.payload["member"].project.name}'
