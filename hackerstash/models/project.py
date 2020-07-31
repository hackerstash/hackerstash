from hackerstash.db import db
from sqlalchemy.types import ARRAY
from hackerstash.models.vote import Vote
from hackerstash.utils.contests import get_contest_name
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
    time_commitment = db.Column(db.String)  # TODO

    business_models = db.Column(ARRAY(db.String))
    fundings = db.Column(ARRAY(db.String))
    platforms_and_devices = db.Column(ARRAY(db.String))

    members = db.relationship('Member', backref='project', cascade='all,delete')
    invites = db.relationship('Invite', backref='project', cascade='all,delete')
    posts = db.relationship('Post', backref='project', cascade='all,delete')
    votes = db.relationship('Vote', backref='project', cascade='all,delete')

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

    def vote(self, user, direction):
        score = 10 if direction == 'up' else -10
        existing_vote = next((x for x in self.votes if x.user.id == user.id), None)

        if existing_vote:
            db.session.delete(existing_vote)
        else:
            vote = Vote(
                type='project',
                contest=get_contest_name(),
                score=score,
                user=user
            )
            self.votes.append(vote)
        db.session.commit()

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
