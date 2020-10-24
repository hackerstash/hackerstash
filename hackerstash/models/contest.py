import datetime
from hackerstash.db import db
from hackerstash.lib.logging import Logging
from hackerstash.models.past_result import PastResult
from hackerstash.models.project import Project

log = Logging(module='Models::Contest')


class Contest(db.Model):
    __tablename__ = 'contests'

    id = db.Column(db.Integer, primary_key=True)

    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    tournament = db.Column(db.Integer, unique=True)
    past_results = db.relationship('PastResult', backref='contest', cascade='all,delete')

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self) -> str:
        return f'<Contest {self.year}_{self.month}>'

    @property
    def is_current(self):
        now = datetime.datetime.now()
        return self.month == now.month and self.year == now.year

    @property
    def winner(self):
        projects = sorted(self.past_results, key=lambda x: x.score, reverse=True)
        return projects[0] if len(projects) else None

    @property
    def start_date(self):
        return datetime.datetime(self.year, self.month, 1)

    @property
    def end_date(self):
        next_month = datetime.datetime(self.year, self.month + 1, 1)
        return next_month - datetime.timedelta(days=1, hours=23, minutes=59, seconds=59)

    @classmethod
    def previous(cls):
        previous = cls.query.order_by(cls.created_at.desc()).limit(1).all()
        return previous[0] if len(previous) else None

    @classmethod
    def find_or_create(cls, month, year):
        log.info('Trying to find contest', {'month': month, 'year': year})
        exists = cls.query.filter_by(year=year, month=month).first()
        if exists:
            log.info('Contest exists', {'contest_id': exists.id})
            return exists
        else:
            previous = cls.previous()
            log.info('Contest does not exist')
            new = cls(month=month, year=year, tournament=previous.tournament if previous else 1)
            db.session.add(new)
            db.session.commit()
            return new

    @classmethod
    def end(cls, month=None, year=None) -> None:
        now = datetime.datetime.now()

        # Get the current contest
        contest = cls.find_or_create(now.month, now.year)

        # Get the leaderboard as it stands
        projects = Project.query.filter_by(published=True).all()
        projects = sorted(projects, key=lambda x: x.vote_score, reverse=True)

        # Fill in the past results
        for index, project in enumerate(projects):
            past_result = PastResult(rank=index, score=project.vote_score, contest=contest, project=project)
            db.session.add(past_result)

        # Create next months tournament
        args = {'month': month + 1, 'year': year, 'tournament': contest.tournament + 1}
        log.info('Creating a new contest', {'contest_args': args})
        new_contest = cls(**args)
        db.session.add(new_contest)
        db.session.commit()

    @classmethod
    def get_current(cls):
        now = datetime.datetime.now()
        return cls.query.filter_by(month=now.month, year=now.year).first()

