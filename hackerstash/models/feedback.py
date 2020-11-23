from hackerstash.db import db
from hackerstash.utils.contest import get_week_and_year


class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True)

    feedback = db.Column(db.String)
    position = db.Column(db.String)

    goals = db.relationship('Goal', backref='goals', cascade='all,delete')

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self) -> str:
        return f'<Feedback {self.id}>'

    @property
    def week(self):
        """
        Get the week the feedback was created at
        :return: int
        """
        return self.created_at.isocalendar()[1]

    @property
    def year(self):
        """
        Get the year the feedback was created at
        :return: int
        """
        return self.created_at.year

    @property
    def current(self) -> bool:
        """
        Return if the feedback is from the current week
        :return: bool
        """
        week, year = get_week_and_year()
        return week == self.week and year and self.year

    @property
    def reviewer(self):
        """
        Return the project that is reviewing this feedbac
        :return: Project
        """
        return self.project

    @property
    def reviewee(self):
        """
        Return the project that is being reviewed
        :return: Project
        """
        return self.goals[0].project
