from hackerstash.db import db
from hackerstash.lib.challenges.helpers import challenge_types, get_score_for_key, get_max_count_for_key
from hackerstash.utils.helpers import find_in_list
from hackerstash.utils.contest import get_week_and_year


class Challenge(db.Model):
    __tablename__ = 'challenges'

    id = db.Column(db.Integer, primary_key=True)

    key = db.Column(db.String)
    count = db.Column(db.Integer, nullable=False)
    max = db.Column(db.Integer, nullable=False)

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self) -> str:
        return f'<Challenge {self.id}>'

    def __init__(self, key, project):
        self.key = key
        self.count = 0
        self.max = get_max_count_for_key(key)
        self.project = project

    def inc(self):
        if not self.complete:
            self.count += 1

    @property
    def week(self):
        return self.created_at.isocalendar()[1]

    @property
    def year(self):
        return self.created_at.year

    @property
    def complete(self):
        return self.count >= self.max

    @property
    def score(self):
        return self.count * get_score_for_key(self.key)

    @property
    def is_current_contest(self):
        week, year = get_week_and_year()
        return week == self.week and year == self.year

    @classmethod
    def has_completed_key(cls, project, key: str) -> bool:
        challenge = Challenge.get_by_key_and_week(project, key)
        return challenge.complete if challenge else False

    @classmethod
    def find_or_create(cls, project, key: str):
        exists = Challenge.get_by_key_and_week(project, key)

        if exists:
            return exists
        else:
            challenge = Challenge(key, project)
            db.session.add(challenge)
            db.session.commit()
            return challenge

    @classmethod
    def get_weekly_challenges_for_project(cls, project):
        out = []
        challenges = project.challenges
        for c in challenge_types:
            out.append(find_in_list(challenges, lambda x: x.key == c and x.is_current_contest))
        return out

    @classmethod
    def get_completed_challenges_for_project(cls, project):
        out = []
        challenges = project.challenges
        for c in challenge_types:
            completed = find_in_list(challenges, lambda x: x.key == c and x.is_current_contest and x.complete)
            if completed:
                out.append(completed)
        return out

    @classmethod
    def get_by_key_and_week(cls, project, key: str, week=None):
        week = week or get_week_and_year()[0]
        return find_in_list(project.challenges, lambda x: x.key == key and x.week == week)
