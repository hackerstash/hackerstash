from flask import render_template
from hackerstash.config import config
from hackerstash.lib.emails.base import Base


class SubscriptionRenewed(Base):
    def __init__(self, email: str, payload: dict) -> None:
        super().__init__(email, payload)

    @property
    def type(self) -> str:
        return 'SUBSCRIPTION_RENEWED'

    @property
    def body(self) -> str:
        args = {**self.payload, 'host': config['host']}
        return render_template('emails/subscription_renewed.html', **args)

    @property
    def text(self) -> str:
        return 'We have successfully processed your recurring (monthly) payment for the HackerStash community'

    @property
    def subject(self) -> str:
        start_date = self.payload['invoice']['start_date']
        return f'😊 Receipt for Subscription Payment {start_date}'
