from flask import render_template
from hackerstash.lib.emails.base import Base


class CloseAccount(Base):
    def __init__(self, email, payload):
        super().__init__(email, payload)

    @property
    def type(self):
        return 'CLOSE_ACCOUNT'

    @property
    def body(self):
        return render_template('emails/close_account.html')

    @property
    def text(self):
        return 'Account Deletion Confirmed'

    @property
    def subject(self):
        return 'Account Deletion Confirmed'
