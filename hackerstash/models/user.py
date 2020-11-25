import json
import arrow
from flask import url_for
from hackerstash.db import db
from hackerstash.lib.redis import redis
from hackerstash.models.tag import Tag, groups
from hackerstash.utils.helpers import html_to_plain_text

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
    reviews = db.relationship('Review', backref='user', cascade='all,delete')

    notifications = db.relationship('Notification', backref='user', cascade='all,delete')
    notifications_settings = db.relationship('NotificationSetting', backref='user', uselist=False, cascade='all,delete')

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self) -> str:
        return f'<User {self.username or self.email}>'

    def __init__(self,  email: str, first_name: str = None, last_name: str = None, avatar: str = None) -> None:
        """
        Create a new user
        :param email: str
        :param first_name: str | None
        :param last_name: str | None
        :param avatar: str | None
        """
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.avatar = avatar
        # Follow a bunch of default tags
        [Tag.query.get(i).follow(self) for i in [1, 2, 3, 4]]

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
        """
        Follow a user
        :param user: User
        :return: User
        """
        if not self.is_following(user):
            self.following.append(user)
            return self

    def unfollow(self, user):
        """
        Unfollow a user
        :param user: User
        :return: User
        """
        if self.is_following(user):
            self.following.remove(user)
            return self

    def is_following(self, user) -> bool:
        """
        Return whether or not this user follows a  user
        :param user: User
        :return: bool
        """
        following = False
        for f in self.following:
            if f.id == user.id:
                following = True
        return following

    @property
    def plain_text_description(self) -> str:
        """
        Get the plain text version of the users bio
        :return: str
        """
        return html_to_plain_text(self.bio, limit=240)

    @property
    def unread_notifications(self) -> list:
        """
        Get a list of unread notifications
        :return: [Notification]
        """
        return list(filter(lambda x: not x.read, self.notifications))

    @property
    def can_post(self) -> bool:
        """
        Return whether or not a user is allowed to posta
        :return: bool
        """
        if self.admin:
            return True
        return self.member and self.member.project.published

    @property
    def project(self):
        """
        Return the users project
        :return: Project
        """
        if self.member:
            return self.member.project

    @property
    def preview_json(self) -> str:
        """
        Get the json string for the users preview card
        :return: str
        """
        data = {
            'name': f'{self.first_name} {self.last_name}',
            'avatar': self.avatar,
            'description': self.plain_text_description,
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
    def recent_completed_challenge(self) -> str:
        """
        Return a recently completed challenge id
        :return: str
        """
        if self.member:
            challenge = redis.get(f'{self.member.project.id}:challenge_completed')
            return challenge.decode('utf-8') if challenge else None

    @classmethod
    def username_exists(cls, username: str) -> bool:
        """
        Return whether or not a username is taken
        :param username: str
        :return: bool
        """
        user = User.query.filter_by(username=username).first()
        return user is not None

    @property
    def group_ids(self) -> list[int]:
        """
        Return a list of group ids that a user belongs to
        :return: list[int]
        """
        # Get a list of tuples like (tag_id, user_id)
        results = db.session.query(groups).filter(groups.c.user_id == self.id).all()
        # Return only the tag ids
        return [x[0] for x in results]
