import json
import arrow
from hackerstash.db import db
from sqlalchemy.types import ARRAY
from hackerstash.lib.challenges.counts import ChallengeCount
from hackerstash.models.challenge import Challenge
from hackerstash.models.vote import Vote
from hackerstash.utils.prizes import get_prize_data_for_position
from hackerstash.utils.votes import sum_of_project_votes

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

    members = db.relationship('Member', backref='project', cascade='all,delete')
    invites = db.relationship('Invite', backref='project', cascade='all,delete')
    posts = db.relationship('Post', backref='project', cascade='all,delete')
    votes = db.relationship('Vote', backref='project', cascade='all,delete')
    past_results = db.relationship('PastResult', backref='project')
    challenges = db.relationship('Challenge', backref='project', cascade='all,delete')
    progress = db.relationship('Progress', backref='project', cascade='all,delete')
    progress_settings = db.relationship('ProgressSetting', backref='project', cascade='all,delete', uselist=False)

    published = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self) -> str:
        return f'<Project {self.name}>'

    def has_member(self, user):
        if not user:
            return False
        match = list(filter(lambda x: x.user.id == user.id, self.members))
        return len(match) > 0

    def has_voted(self, user):
        return next((x for x in self.votes if x.user.id == user.id), None)

    def vote(self, user, direction):
        score = 10 if direction == 'up' else -10
        existing_vote = self.has_voted(user)

        if existing_vote:
            db.session.delete(existing_vote)
        else:
            vote = Vote(type='project', score=score, user=user)
            self.votes.append(vote)
        db.session.commit()

    def has_member_with_email(self, email) -> bool:
        member = next((x for x in self.members if x.user.email == email), None)
        return bool(member)

    def vote_status(self, user):
        if not user:
            return 'disabled logged-out'

        if not user.member or not user.member.project.published:
            return 'disabled not-published'

        if self.id == user.member.project.id:
            return 'disabled own-project'

        existing_vote = self.has_voted(user)

        if existing_vote:
            return 'upvoted' if existing_vote.score > 0 else 'downvoted'
        return None

    @property
    def position(self) -> int:
        if not self.published:
            return -1
        # NOTICE: Be aware that calling this will make an additional
        # call to the database! Don't use it in a loop
        projects = self.query.filter_by(published=True).all()
        projects = sorted(projects, key=lambda x: x.vote_score, reverse=True)
        # Where is Array.findIndex() 🤦‍
        return [index for index, project in enumerate(projects) if project.id == self.id][0] + 1

    @property
    def vote_score(self) -> int:
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
        votes = list(filter(lambda x: x.score > 0, self.all_votes))
        return len(votes)

    @property
    def downvotes(self) -> int:
        votes = list(filter(lambda x: x.score < 0, self.all_votes))
        return len(votes)

    @property
    def preview_json(self) -> str:
        data = {
            'name': self.name,
            'avatar': self.avatar,
            'description': self.description,
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
        out = []
        votes = self.all_votes
        start_of_week = arrow.now().floor('week')
        for i in range(7):
            this_day = start_of_week.shift(days=+i)
            matching_votes = list(filter(lambda x: x.created_at.day == this_day.day, votes))
            out.append(len(matching_votes))
        return json.dumps(out)

    def create_or_inc_challenge(self, key: str):
        challenge = Challenge.find_or_create(self, key)
        challenge.inc()
        db.session.commit()

    @property
    def number_of_completed_challenges(self):
        challenge_counts = ChallengeCount(self.challenges)
        return len(challenge_counts.completed_challenges_for_the_week)

    @property
    def prize(self):
        return get_prize_data_for_position(self.position - 1)  # Not 0 indexed
