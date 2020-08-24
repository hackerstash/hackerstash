from hackerstash.db import db
from hackerstash.utils.contest import get_week_and_year


class Vote(db.Model):
    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True)

    type = db.Column(db.String)
    contest = db.Column(db.String)
    score = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self) -> str:
        return f'<Vote {self.id}>'

    @property
    def week(self):
        return self.created_at.isocalendar()[1]

    @property
    def year(self):
        return self.created_at.year

    @property
    def is_current_contest(self):
        week, year = get_week_and_year()
        return week == self.week and year == self.year
