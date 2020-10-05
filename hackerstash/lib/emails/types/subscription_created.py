from flask import render_template
from hackerstash.config import config
from hackerstash.lib.emails.base import Base


class SubscriptionCreated(Base):
    def __init__(self, email: str, payload: dict) -> None:
        super().__init__(email, payload)

    @property
    def type(self) -> str:
        return 'SUBSCRIPTION_CREATED'

    @property
    def body(self) -> str:
        args = {**self.payload, 'host': config['host']}
        return render_template('emails/subscription_created.html', **args)

    @property
    def text(self) -> str:
        project_name = self.payload['member'].project.name
        return f'We have successfully processed your subscription and {project_name} is now published on Hackerstash'

    @property
    def subject(self) -> str:
        return 'Your Project Has Been Published 🙌'
