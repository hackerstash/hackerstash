from hackerstash.db import db
from hackerstash.utils.contest import get_week_and_year


class Goal(db.Model):
    __tablename__ = 'goals'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean)
    evidence = db.Column(db.String)

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    feedback_id = db.Column(db.Integer, db.ForeignKey('feedback.id'))

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self) -> str:
        return f'<Goal {self.id}>'

    @property
    def week(self) -> int:
        """
        Return the week this goal was created at
        :return: int
        """
        return self.created_at.isocalendar()[1]

    @property
    def year(self) -> int:
        """
        Return the year this goal was created at
        :return: int
        """
        return self.created_at.year

    @property
    def current(self) -> bool:
        """
        Return if the goal is from this week
        :return: bool
        """
        week, year = get_week_and_year()
        return week == self.week and year and self.year
