import json
from flask import url_for
from sqlalchemy.types import ARRAY
from hackerstash.db import db
from hackerstash.lib.logging import Logging
from hackerstash.lib.redis import redis
from hackerstash.lib.project_score_data import build_weekly_vote_data
from hackerstash.lib.prizes import Prizes
from hackerstash.models.challenge import Challenge
from hackerstash.models.vote import Vote
from hackerstash.utils.helpers import find_in_list, html_to_plain_text
from hackerstash.utils.votes import sum_of_project_votes

log = Logging(module='Models::Project')
# There are a lof of horrifically unperformant
# things in here, they are all done in the name
# of speed


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

    stash = db.Column(db.Integer)

    members = db.relationship('Member', backref='project', cascade='all,delete')
    invites = db.relationship('Invite', backref='project', cascade='all,delete')
    posts = db.relationship('Post', backref='project', cascade='all,delete')
    votes = db.relationship('Vote', backref='project', cascade='all,delete', lazy='joined')
    past_results = db.relationship('PastResult', backref='project')
    challenges = db.relationship('Challenge', backref='project', cascade='all,delete')
    transactions = db.relationship('Transaction', backref='project', cascade='all,delete')
    subscriptions = db.relationship('Subscription', backref='project', cascade='all,delete')

    ghost = db.Column(db.Boolean, default=False)
    published = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self) -> str:
        return f'<Project {self.name}>'

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
            # Projects are different as you can revote on them every week
            lambda x: x.user.member.project.id == user.member.project.id and x.is_current_contest
        )

    def vote(self, user, direction):
        score = 10 if direction == 'up' else -10
        existing_vote = self.get_existing_vote_for_user(user)

        if existing_vote:
            db.session.delete(existing_vote)
        else:
            vote = Vote(type='project', score=score, user=user)
            self.votes.append(vote)
        db.session.commit()

    def vote_status(self, user):
        if not user:
            return 'disabled logged-out'
        if not user.member or not user.member.project.published:
            return 'disabled not-published'
        if self.id == user.member.project.id:
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
        # This is an awful design and is very expensive, so
        # shove it in redis for a minute. At some point we
        # should probably think about having projects own all
        # the votes and not the posts/comments
        if leaderboard := redis.get('leaderboard'):
            leaderboard = json.loads(leaderboard)
        else:
            projects = self.query.filter_by(published=True).all()
            projects = sorted(projects, key=lambda x: x.vote_score, reverse=True)
            leaderboard = {}
            for index, project in enumerate(projects):
                leaderboard[str(project.id)] = index + 1
            redis.set('leaderboard', json.dumps(leaderboard), ex=60)
        return leaderboard.get(str(self.id), -1)

    @property
    def vote_score(self) -> int:
        # The project vote score behaves a bit differently to posts
        # and comments as it only totals the scores for this week
        return sum_of_project_votes(self)

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
        return json.dumps(build_weekly_vote_data(self))

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

    @property
    def prize(self):
        # Not 0 indexed
        return Prizes.get_for_position(self.position - 1)

    def add_funds(self, value):
        if not self.stash:
            self.stash = 0
        self.stash += value
        log.info('Adding funds to stash', {'project_id': self.id, 'new_total': self.stash})

    def remove_funds(self, value):
        if (self.stash - value) < 0:
            log.warn('Unable to remove funds from stash', {'project_id': self.id, 'value': value, 'stash': self.stash})
        else:
            self.stash -= value
            log.info('Removing funds from stash', {'project_id': self.id, 'new_total': self.stash})
