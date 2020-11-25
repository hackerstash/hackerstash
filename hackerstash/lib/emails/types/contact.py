from flask import render_template
from hackerstash.config import config
from hackerstash.lib.emails.base import Base


class Contact(Base):
    def __init__(self, email: str, payload: dict) -> None:
        """
        Initialise an instance of the Contact class
        :param email: str
        :param payload: dict
        """
        super().__init__(email, payload)

    @property
    def type(self) -> str:
        """
        Return the email type
        :return: str
        """
        return 'CONTACT'

    @property
    def body(self) -> str:
        """
        Return the rendered email
        :return: str
        """
        return render_template('emails/contact.html', **self.payload, host=config['host'])

    @property
    def text(self) -> str:
        """
        Return the plain text version of the email
        :return: str
        """
        return 'Contact Form'

    @property
    def subject(self) -> str:
        """
        Return the subject for the email
        :return: str
        """
        return 'Contact Form'
