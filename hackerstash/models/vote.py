import datetime
from hackerstash.db import db


class Vote(db.Model):
    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True)

    type = db.Column(db.String)
    score = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self) -> str:
        return f'<Vote {self.id}>'

    # The default order should be newest first
    __mapper_args__ = {
        'order_by': created_at.desc()
    }

    @property
    def month(self) -> int:
        """
        Return the month this vote was created at
        :return: int
        """
        return self.created_at.month

    @property
    def year(self) -> int:
        """
        Return the year this vote was created at
        :return: int
        """
        return self.created_at.year

    @property
    def is_current_contest(self) -> bool:
        """
        Return whether this vote is from the current tournament
        :return: bool
        """
        now = datetime.datetime.now()
        return now.month == self.month and now.year == self.year
