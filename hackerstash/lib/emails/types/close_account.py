from flask import render_template
from hackerstash.config import config
from hackerstash.lib.emails.base import Base


class CloseAccount(Base):
    def __init__(self, email: str, payload: dict) -> None:
        super().__init__(email, payload)

    @property
    def type(self) -> str:
        return 'CLOSE_ACCOUNT'

    @property
    def body(self) -> str:
        return render_template('emails/close_account.html', host=config['host'])

    @property
    def text(self) -> str:
        return 'Account Deletion Confirmed'

    @property
    def subject(self) -> str:
        return 'Account Deletion Confirmed'
