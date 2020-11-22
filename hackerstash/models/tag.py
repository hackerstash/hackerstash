from hackerstash.db import db


groups = db.Table(
    'users_groups',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String)
    description = db.Column(db.String)

    icon = db.Column(db.String)
    icon_color = db.Column(db.String)
    background_color = db.Column(db.String)

    post = db.relationship('Post', backref='tag')
    members = db.relationship('User', secondary=groups, backref='tag')

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self) -> str:
        return f'<Tag {self.name}>'

    def has_user(self, user) -> bool:
        """
        Return whether this user is a member of this group
        :param user: User
        :return: bool
        """
        following = False
        for f in self.members:
            if f.id == user.id:
                following = True
        return following

    def follow(self, user) -> None:
        """
        Follow this group
        :param user: User
        :return: None
        """
        if not self.has_user(user):
            self.members.append(user)

    def unfollow(self, user) -> None:
        """
        Unfollow this group
        :param user: User
        :return: None
        """
        if self.has_user(user):
            self.members.remove(user)
