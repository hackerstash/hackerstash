import json
import arrow
from flask import url_for
from hackerstash.db import db
from hackerstash.lib.redis import redis
from hackerstash.utils.filters import to_plain_text

follow = db.Table(
    'users_following',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String)
    last_name = db.Column(db.String)

    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True, nullable=False)
    admin = db.Column(db.Boolean, default=False)

    bio = db.Column(db.String)
    location = db.Column(db.String)
    provider = db.Column(db.String)
    telephone = db.Column(db.String)
    twitter = db.Column(db.String)
    avatar = db.Column(db.String)

    member = db.relationship('Member', backref='user', uselist=False, cascade='all,delete')
    comments = db.relationship('Comment', backref='user', cascade='all,delete')
    posts = db.relationship('Post', backref='user', cascade='all,delete')
    votes = db.relationship('Vote', backref='user', cascade='all,delete')

    notifications = db.relationship('Notification', backref='user', cascade='all,delete')
    notifications_settings = db.relationship('NotificationSetting', backref='user', uselist=False, cascade='all,delete')

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self) -> str:
        return f'<User {self.username or self.email}>'

    following = db.relationship(
        'User',
        secondary=follow,
        primaryjoin=(follow.c.follower_id == id),
        secondaryjoin=(follow.c.followed_id == id),
        backref='users_following'
    )

    followers = db.relationship(
        'User',
        secondary=follow,
        primaryjoin=(follow.c.followed_id == id),
        secondaryjoin=(follow.c.follower_id == id),
        viewonly=True
    )

    def follow(self, user):
        if not self.is_following(user):
            self.following.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)
            return self

    def is_following(self, user):
        following = False

        for f in self.following:
            if f.id == user.id:
                following = True

        return following

    @property
    def unread_notifications(self):
        return list(filter(lambda x: not x.read, self.notifications))

    @property
    def can_post(self):
        if self.admin:
            return True
        return self.member and self.member.project.published

    @property
    def preview_json(self) -> str:
        data = {
            'name': f'{self.first_name} {self.last_name}',
            'avatar': self.avatar,
            'description': to_plain_text(self.bio, limit=240),
            'admin': self.admin,
            'url': url_for('users.show', user_id=self.id),
            'lists': [
                {
                    'key': 'Username',
                    'value': f'@{self.username}'
                },
                {
                    'key': 'Project',
                    'value': self.member.project.name if self.member else 'None'
                },
                {
                    'key': 'Joined',
                    'value': arrow.get(self.created_at).humanize()
                },
                {
                    'key': 'Location',
                    'value': self.location or 'Unknown'
                }
            ]

        }
        return json.dumps(data)

    @property
    def recent_completed_challenge(self):
        if self.member:
            challenge = redis.get(f'{self.member.project.id}:challenge_completed')
            return challenge.decode('utf-8') if challenge else None
