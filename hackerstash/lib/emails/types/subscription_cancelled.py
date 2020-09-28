from flask import render_template
from hackerstash.config import config
from hackerstash.lib.emails.base import Base


class SubscriptionCancelled(Base):
    def __init__(self, email: str, payload: dict) -> None:
        super().__init__(email, payload)

    @property
    def type(self) -> str:
        return 'SUBSCRIPTION_CANCELLED'

    @property
    def body(self) -> str:
        args = {**self.payload, 'host': config['host']}
        return render_template('emails/subscription_cancelled.html', **args)

    @property
    def text(self) -> str:
        return 'We\'re emailing to confirm that we have successfully cancelled your subscription \
        to the HackerStash community. Your project is no longer published and you will not be \
        entitled to any further tournament prizes.'

    @property
    def subject(self) -> str:
        return 'HackerStash Community Subscription Cancelled 😢'
