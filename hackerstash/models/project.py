import json
from hackerstash.db import db
from sqlalchemy.types import ARRAY
from hackerstash.models.vote import Vote
from hackerstash.utils.votes import sum_of_project_votes


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

    published = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
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

    def has_member_with_email(self, email):
        member = next((x for x in self.members if x.user.email == email), None)
        return bool(member)

    def vote_status(self, user):
        if self.has_member(user):
            return 'disabled'

        existing_vote = self.has_voted(user)

        if existing_vote:
            return 'upvoted' if existing_vote.score > 0 else 'downvoted'
        return None

    @property
    def position(self):
        if not self.published:
            return -1
        # NOTICE: Be aware that calling this will make an additional
        # call to the database! Don't use it in a loop
        projects = self.query.filter_by(published=True).all()
        projects = sorted(projects, key=lambda x: x.vote_score, reverse=True)
        # Where is Array.findIndex() 🤦‍
        return [index for index, project in enumerate(projects) if project.id == self.id][0] + 1

    @property
    def vote_score(self):
        return sum_of_project_votes(self)

    @property
    def upvotes(self):
        votes = list(filter(lambda x: x.score > 0, self.votes))
        return len(votes)

    @property
    def downvotes(self):
        votes = list(filter(lambda x: x.score < 0, self.votes))
        return len(votes)

    @property
    def preview_json(self):
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
