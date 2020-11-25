from flask import render_template
from hackerstash.config import config
from hackerstash.lib.emails.base import Base


class ProjectVoteReminder(Base):
    def __init__(self, email: str, payload: dict) -> None:
        """
        Initialise an instance of the ProjectVoteReminder class
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
        return 'PROJECT_VOTE_REMINDER'

    @property
    def body(self) -> str:
        """
        Return the rendered email
        :return: str
        """
        return render_template('emails/project_vote_reminder.html', **self.payload, host=config['host'])

    @property
    def text(self) -> str:
        """
        Return the plain text version of the email
        :return: str
        """
        return 'You have 3 days remaining to upvote your top 3 projects'

    @property
    def subject(self) -> str:
        """
        Return the subject for the email
        :return: str
        """
        return 'You have 3 days remaining to upvote your top 3 projects'
