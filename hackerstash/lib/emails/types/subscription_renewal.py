from flask import render_template
from hackerstash.config import config
from hackerstash.lib.emails.base import Base
from hackerstash.utils.filters import to_contest_date


class SubscriptionRenewal(Base):
    def __init__(self, email: str, payload: dict) -> None:
        super().__init__(email, payload)

    @property
    def type(self) -> str:
        return 'SUBSCRIPTION_RENEWAL'

    @property
    def body(self) -> str:
        args = {**self.payload, 'host': config['host']}
        return render_template('emails/subscription_renewal.html', **args)

    @property
    def text(self) -> str:
        return 'This is a friendly reminder that your HackerStash community subscription will automatically renew soon.'

    @property
    def subject(self) -> str:
        renew_date = self.payload['subscription']['renew_date']
        return f'😇 Subscription Renewal Reminder {to_contest_date(renew_date)}'
