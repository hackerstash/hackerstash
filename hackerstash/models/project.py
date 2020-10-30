import json
from flask import url_for
from sqlalchemy.types import ARRAY
from hackerstash.db import db
from sqlalchemy import func, select
from sqlalchemy.ext.hybrid import hybrid_property
from hackerstash.lib.leaderboard import Leaderboard
from hackerstash.lib.logging import Logging
from hackerstash.lib.project_score_data import build_monthly_vote_data
from hackerstash.models.challenge import Challenge
from hackerstash.models.member import Member
from hackerstash.models.vote import Vote
from hackerstash.utils.helpers import find_in_list, html_to_plain_text

log = Logging(module='Models::Project')


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
    url = db.Column(db.String)
    description = db.Column(db.String)

    avatar = db.Column(db.String)

    location = db.Column(db.String)
    start_month = db.Column(db.Integer)
    start_year = db.Column(db.Integer)
    time_commitment = db.Column(db.String)

    business_models = db.Column(ARRAY(db.String))
    fundings = db.Column(ARRAY(db.String))
    platforms_and_devices = db.Column(ARRAY(db.String))

    members = db.relationship('Member', backref='project', cascade='all,delete')
    invites = db.relationship('Invite', backref='project', cascade='all,delete')
    posts = db.relationship('Post', backref='project', cascade='all,delete')
    votes = db.relationship('Vote', backref='project', cascade='all,delete', lazy='joined')
    past_results = db.relationship('PastResult', backref='project')
    challenges = db.relationship('Challenge', backref='project', cascade='all,delete')
    reviews = db.relationship('Review', backref='project', cascade='all,delete')

    ghost = db.Column(db.Boolean, default=False)
    published = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self) -> str:
        return f'<Project {self.name}>'

    @hybrid_property
    def team_size(self):
        return sum(self.members)

    @team_size.expression
    def team_size(cls):
        return select([func.sum(Member.id)]).where(Member.project_id == cls.id).label('team_size')

    def has_member(self, user):
        member = self.get_member_by_id(user.id if user else None)
        return bool(member)

    def get_member_by_id(self, user_id=None):
        return find_in_list(self.members, lambda x: x.user.id == user_id)

    def has_member_with_email(self, email):
        return find_in_list(self.members, lambda x: x.user.email == email)

    def get_existing_vote_for_user(self, user):
        # Although a user clicked on the button, the
        # vote is actually made on behalf of the project
        # to stop people from creating 30 fake users and
        # downvote bombing other users
        return find_in_list(
            self.votes,
            # Projects are different as you can revote on them every month
            lambda x: x.user.project.id == user.project.id and x.is_current_contest
        )

    def vote(self, user, direction):
        score = 10 if direction == 'up' else -10
        existing_vote = self.get_existing_vote_for_user(user)
        # Update the leaderboard
        Leaderboard(self).update(score)

        if existing_vote:
            db.session.delete(existing_vote)
        else:
            vote = Vote(type='project', score=score, user=user)
            self.votes.append(vote)
        db.session.commit()

    def vote_status(self, user):
        if not user:
            return 'disabled logged-out'
        if not user.member or not user.project.published:
            return 'disabled not-published'
        if self.id == user.project.id:
            return 'disabled own-project'

        existing_vote = self.get_existing_vote_for_user(user)
        return ('upvoted' if existing_vote.score > 0 else 'downvoted') if existing_vote else ''

    @property
    def plain_text_description(self):
        return html_to_plain_text(self.description, limit=240)

    @property
    def position(self) -> int:
        if not self.published:
            return -1
        return Leaderboard(self).position

    @property
    def vote_score(self) -> int:
        return Leaderboard(self).score

    @property
    def all_votes(self):
        out = []
        # All the project votes
        [out.append(v) for v in self.votes]
        # all the post votes
        for p in self.posts:
            [out.append(v) for v in p.votes]
        # all the comment votes
        for m in self.members:
            for c in m.user.comments:
                [out.append(v) for v in c.votes]
        return out

    @property
    def upvotes(self) -> int:
        # Get all the votes for this contest that have a
        # positive score, therefore being an upvote
        votes = [vote for vote in self.all_votes if vote.is_current_contest and vote.score > 0]
        return len(votes)

    @property
    def downvotes(self) -> int:
        # Get all the votes for this contest that have a
        # negative score, therefore being a downvote
        votes = [vote for vote in self.all_votes if vote.is_current_contest and vote.score < 0]
        return len(votes)

    @property
    def preview_json(self) -> str:
        data = {
            'name': self.name,
            'avatar': self.avatar,
            'description': self.plain_text_description,
            'url': url_for('projects.show', project_id=self.id),
            'lists': [
                {
                    'key': 'Tournament position',
                    'value': self.position
                },
                {
                    'key': 'Points',
                    'value': self.vote_score
                },
                {
                    'key': 'Team members',
                    'value': len(self.members)
                },
                {
                    'key': 'Website (URL)',
                    'value': self.url
                }
            ]

        }
        return json.dumps(data)

    @property
    def project_score_data(self):
        return json.dumps(build_monthly_vote_data(self))

    def create_or_inc_challenge(self, key: str):
        challenge = Challenge.find_or_create(self, key)
        challenge.inc()
        db.session.commit()

    def create_or_set_challenge(self, key: str, value: int):
        challenge = Challenge.find_or_create(self, key)
        challenge.count = value
        db.session.commit()

    @property
    def number_of_completed_challenges(self):
        completed = Challenge.get_completed_challenges_for_project(self)
        return len(completed)
