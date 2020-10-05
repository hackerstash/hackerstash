from flask import render_template
from hackerstash.config import config
from hackerstash.lib.emails.base import Base


class CashOutRequest(Base):
    def __init__(self, email: str, payload: dict) -> None:
        super().__init__(email, payload)

    @property
    def type(self) -> str:
        return 'CASH_OUT_REQUEST'

    @property
    def body(self) -> str:
        return render_template('emails/cash_out_request.html', **self.payload, host=config['host'])

    @property
    def text(self) -> str:
        return 'Cash Out Request'

    @property
    def subject(self) -> str:
        return 'Cash Out Request'
