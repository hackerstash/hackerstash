import jwt
from flask import url_for
from hackerstash.db import db
from hackerstash.config import config
from hackerstash.models.invite import Invite
from hackerstash.models.member import Member
from hackerstash.lib.notifications.factory import notification_factory


def generate_invite_link(email: str) -> str:
    token = jwt.encode({'email': email}, config['secret'], algorithm='HS256')
    # jwt.encode returns bytes
    return config['host'] + url_for('projects.accept_invite', invite_token=token.decode('utf-8'))


def decrypt_invite_link(token: str) -> dict:
    return jwt.decode(token, config['secret'], algorithm='HS256')


def verify_invite(user) -> None:
    invite = Invite.query.filter_by(email=user.email).first()

    if invite:
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
