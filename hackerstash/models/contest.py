import datetime
from sqlalchemy.types import JSON
from hackerstash.db import db
from hackerstash.lib.logging import logging
from hackerstash.lib.notifications.factory import notification_factory
from hackerstash.models.past_result import PastResult
from hackerstash.models.project import Project
from hackerstash.models.transaction import Transaction
from hackerstash.utils.contest import get_week_and_year


class Contest(db.Model):
    __tablename__ = 'contests'

    id = db.Column(db.Integer, primary_key=True)

    year = db.Column(db.Integer)
    week = db.Column(db.Integer)
    tournament = db.Column(db.Integer, unique=True)
    past_results = db.relationship('PastResult', backref='contest', cascade='all,delete')

    top_up = db.Column(db.Integer)
    prizes = db.Column(JSON(none_as_null=True))

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __init__(self, week, year, tournament):
        self.week = week
        self.year = year
        self.tournament = tournament
        self.top_up = 0
        self.prizes = {}

        for i in range(200):
            self.prizes[f'prize_{i}'] = 0

    def __repr__(self) -> str:
        return f'<Contest {self.year}_{self.week}>'

    @property
    def is_current(self):
        week, year = get_week_and_year()
        return self.week == week

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
        return self.start_date + datetime.timedelta(days=6, hours=23, minutes=59, seconds=59)

    @classmethod
    def previous(cls):
        previous = cls.query.order_by(cls.created_at.desc()).limit(1).all()
        return previous[0] if len(previous) else None

    @classmethod
    def find_or_create(cls, week, year):
        logging.info('Trying to find contest with args %s', {'week': week, 'year': year})
        exists = cls.query.filter_by(year=year, week=week).first()
        if exists:
            logging.info('Contest exists: %s', exists.id)
            return exists
        else:
            previous = cls.previous()
            logging.info('Contest does not exist')
            new = cls(week=week, year=year, tournament=previous.tournament if previous else 1)
            db.session.add(new)
            db.session.commit()
            return new

    @classmethod
    def end(cls, week=None, year=None) -> None:
        now = datetime.datetime.now()

        week = week or datetime.date(now.year, now.month, now.day).isocalendar()[1]
        year = year or now.year

        # Get the current contest
        contest = cls.find_or_create(week, year)

        # Get the leaderboard as it stands
        projects = Project.query.filter_by(published=True).all()
        projects = sorted(projects, key=lambda x: x.vote_score, reverse=True)

        # Fill in the past results
        for index, project in enumerate(projects):
            past_result = PastResult(rank=index, score=project.vote_score, contest=contest, project=project)
            db.session.add(past_result)
            notification_factory('contest_ended', {'past_result': past_result}).publish()
            if past_result.prize['value'] > 0:
                Transaction.add_prize_winnings(past_result)

        # Create next weeks tournament
        args = {'week': week + 1, 'year': year, 'tournament': contest.tournament + 1}
        logging.info('Creating a new contest with args: %s', args)
        new_contest = cls(**args)
        db.session.add(new_contest)
        db.session.commit()

    @classmethod
    def get_current(cls):
        week, year = get_week_and_year()
        return cls.query.filter_by(week=week, year=year).first()

    def get_prize_for_position(self, position: int) -> int:
        return self.prizes.get(f'prize_{position}', 0)
