from flask import render_template
from hackerstash.lib.emails.base import Base


class Contact(Base):
    def __init__(self, email, payload):
        super().__init__(email, payload)

    @property
    def type(self):
        return 'CONTACT'

    @property
    def body(self):
        return render_template('emails/contact.html', **self.payload)

    @property
    def text(self):
        return 'Contact Form'

    @property
    def subject(self):
        return 'Contact Form'
