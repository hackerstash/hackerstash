from hackerstash.db import db
from hackerstash.utils.contest import get_week_and_year


class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True)

    feedback = db.Column(db.String)
    position = db.Column(db.String)

    goals = db.relationship('Goal', backref='goals', cascade='all,delete')
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self) -> str:
        return f'<Feedback {self.id}>'

    @property
    def week(self):
        return self.created_at.isocalendar()[1]

    @property
    def year(self):
        return self.created_at.year

    @property
    def current(self):
        week, year = get_week_and_year()
        return week == self.week and year and self.year
