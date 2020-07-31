from hackerstash.db import db

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

    def __repr__(self):
        return f'<User {self.username or self.email}>'

    following = db.relationship(
        'User',
        secondary=follow,
        primaryjoin=(follow.c.follower_id == id),
        secondaryjoin=(follow.c.followed_id == id),
        backref=db.backref('users_following', lazy='select'),
        lazy='select'
    )

    followers = db.relationship(
        'User',
        secondary=follow,
        primaryjoin=(follow.c.followed_id == id),
        secondaryjoin=(follow.c.follower_id == id),
        backref=db.backref('users_followers', lazy='select'),
        lazy='select'
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
