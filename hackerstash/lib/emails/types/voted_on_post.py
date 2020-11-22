from flask import render_template
from hackerstash.config import config
from hackerstash.lib.emails.base import Base


class VotedOnPost(Base):
    def __init__(self, email: str, payload: dict) -> None:
        """
        Initialise an instance of the VotedOnPost class
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
        return 'VOTED_ON_POST'

    @property
    def body(self) -> str:
        """
        Return the rendered email
        :return: str
        """
        return render_template('emails/voted_on_post.html', **self.payload, host=config['host'])

    @property
    def text(self) -> str:
        """
        Return the plain text version of the email
        :return: str
        """
        return f'Your post was {self.payload["direction"].lower()}voted'

    @property
    def subject(self) -> str:
        """
        Return the subject for the email
        :return: str
        """
        return f'Your post was {self.payload["direction"].lower()}voted'
