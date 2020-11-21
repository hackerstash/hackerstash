import jwt
from flask import url_for
from hackerstash.db import db
from hackerstash.config import config
from hackerstash.models.invite import Invite
from hackerstash.models.member import Member
from hackerstash.models.user import User
from hackerstash.lib.notifications.factory import notification_factory


class Invites:
    @classmethod
    def generate(cls, email: str) -> str:
        """
        Generate an encoded sign up link to be sent in an email
        :param email: str
        :return: str
        """
        token = jwt.encode({'email': email}, config['secret'], algorithm='HS256')
        # jwt.encode returns bytes
        return config['host'] + url_for('projects.accept_invite', invite_token=token.decode('utf-8'))

    @classmethod
    def decode(cls, token: str) -> str:
        """
        Decode the sign up link to extract the email
        :param token: str
        :return: str
        """
        return jwt.decode(token, config['secret'], algorithm='HS256')

    @classmethod
    def verify(cls, user: User) -> None:
        """
        Check if an invite exists for a user, if it does then a new
        member is created and their team is notififed
        :param user: User
        :return: None
        """
        if invite := Invite.query.filter_by(email=user.email).first():
            # User has invited to a project and they
            # didn't yet have an account
            member = Member(
                owner=False,
                role=invite.role,
                user=user,
                project=invite.project
            )
            db.session.add(member)
            db.session.delete(invite)
            db.session.commit()

            notification_factory('member_verified', {'member': member}).publish()
