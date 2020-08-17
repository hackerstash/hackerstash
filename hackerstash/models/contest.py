import datetime
from hackerstash.db import db
from hackerstash.models.past_result import PastResult
from hackerstash.models.project import Project


class Contest(db.Model):
    __tablename__ = 'contests'

    id = db.Column(db.Integer, primary_key=True)

    year = db.Column(db.Integer)
    week = db.Column(db.Integer)
    tournament = db.Column(db.Integer, unique=True)
    past_results = db.relationship('PastResult', backref='contest', cascade='all,delete')

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self) -> str:
        return f'<Contest {self.year}_{self.week}>'

    @property
    def winner(self):
        projects = sorted(self.past_results, key=lambda x: x.score, reverse=True)
        return projects[0] if len(projects) else None

    @property
    def start_date(self):
        date = f'{self.year}-W{self.week}'
        return datetime.datetime.strptime(date + '-1', '%Y-W%W-%w')

    @property
    def end_date(self):
        return self.start_date + + datetime.timedelta(days=6)

    @classmethod
    def previous(cls):
        previous = cls.query.order_by(cls.created_at.desc()).limit(1).all()
        return previous[0] if len(previous) else None

    @classmethod
    def end(cls, week, year) -> None:
        now = datetime.datetime.now()
        previous_contest = cls.previous()

        week = week or datetime.date(now.year, now.month, now.day).isocalendar()[1] - 1
        year = year or now.year
        # We could use autoincrement, but if we cock up and have to delete it
        # we can never go back!
        tournament = previous_contest.tournament + 1 if previous_contest else 1

        # Create the base contest
        contest = cls(year=year, week=week, tournament=tournament)
        db.session.add(contest)
        db.session.commit()

        # Get the leaderboard as it stands
        projects = Project.query.filter_by(published=True).all()
        projects = sorted(projects, key=lambda x: x.vote_score, reverse=True)

        # Fill in the past results
        for index, project in enumerate(projects):
            past_result = PastResult(rank=index, score=project.vote_score, contest=contest, project=project)
            db.session.add(past_result)

        db.session.commit()
