from hackerstash.db import db
from hackerstash.lib.challenges.helpers import challenge_types, get_score_for_key, get_max_count_for_key, mark_as_complete
from hackerstash.lib.leaderboard import Leaderboard
from hackerstash.utils.helpers import find_in_list
from hackerstash.utils.contest import get_week_and_year


class Challenge(db.Model):
    __tablename__ = 'challenges'

    id = db.Column(db.Integer, primary_key=True)

    key = db.Column(db.String)
    count = db.Column(db.Integer, nullable=False)
    max = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self) -> str:
        return f'<Challenge {self.id}>'

    def __init__(self, key: str, project) -> None:
        """
        Initialise an instance of the Challenge model
        :param key: str
        :param project: Project
        """
        self.key = key
        self.count = 0
        self.max = get_max_count_for_key(key)
        self.score = get_score_for_key(key)
        self.project = project

    def inc(self) -> None:
        """
        Increment the challenge by 1 if it is not complete. When
        the challenge is completed, the leaderboard should be
        updated too
        :return: None
        """
        if not self.complete:
            self.count += 1
            if self.complete:
                mark_as_complete(self)
                # Update the leaderboard
                Leaderboard(self.project).update(self.score)

    @property
    def week(self) -> int:
        """
        Get the week the challenge was created at
        :return: int
        """
        return self.created_at.isocalendar()[1]

    @property
    def year(self) -> int:
        """
        Get the year the challenge was created at
        :return: int
        """
        return self.created_at.year

    @property
    def complete(self) -> bool:
        """
        Return whether or not the challenge is complete
        :return: bool
        """
        return self.count >= self.max

    @property
    def is_current_contest(self) -> bool:
        """
        Return whether or not this challenge is from this
        current tournament
        :return:
        """
        week, year = get_week_and_year()
        return week == self.week and year == self.year

    @classmethod
    def has_completed_key(cls, project, key: str) -> bool:
        """
        Return whether or not a challenge is completed by using
        it's key
        :param project: Project
        :param key: str
        :return: bool
        """
        challenge = Challenge.get_by_key_and_week(project, key)
        return challenge.complete if challenge else False

    @classmethod
    def find_or_create(cls, project, key: str):
        """
        Find or create a challenge
        :param project: Project
        :param key: str
        :return: Challenge
        """
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
        """
        Get all the challenges for this week
        :param project: Project
        :return: [Challenge]
        """
        out = []
        challenges = project.challenges
        for c in challenge_types:
            out.append(find_in_list(challenges, lambda x: x.key == c and x.is_current_contest))
        return out

    @classmethod
    def get_completed_challenges_for_project(cls, project):
        """
        Get all of the completed challenges for this week
        :param project: Project
        :return: [Challenge]
        """
        out = []
        challenges = project.challenges
        for c in challenge_types:
            completed = find_in_list(challenges, lambda x: x.key == c and x.is_current_contest and x.complete)
            if completed:
                out.append(completed)
        return out

    @classmethod
    def get_by_key_and_week(cls, project, key: str, week=None):
        """
        Get a challenge by the week and week
        :param project: Project
        :param key: str
        :param week: int
        :return: Challenge
        """
        week = week or get_week_and_year()[0]
        return find_in_list(project.challenges, lambda x: x.key == key and x.week == week)
