from flask import render_template
from hackerstash.config import config
from hackerstash.lib.emails.base import Base


class PrizeAwarded(Base):
    def __init__(self, email: str, payload: dict) -> None:
        super().__init__(email, payload)

    @property
    def type(self) -> str:
        return 'PRIZE_AWARDED'

    @property
    def body(self) -> str:
        return render_template('emails/prize_awarded.html', **self.payload, host=config['host'])

    @property
    def text(self) -> str:
        return 'The results are in...'

    @property
    def subject(self) -> str:
        return 'The results are in...'
