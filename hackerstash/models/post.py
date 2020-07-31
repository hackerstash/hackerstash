from hackerstash.db import db
from hackerstash.models.vote import Vote
from hackerstash.utils.contests import get_contest_name
from hackerstash.utils.votes import sum_of_votes


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', cascade='all,delete')
    votes = db.relationship('Vote', backref='post', cascade='all,delete')

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        return f'<Post {self.title}>'

    def has_author(self, user):
        if not user:
            return None

        return self.user.id == user.id

    def vote(self, user, direction):
        score = 5 if direction == 'up' else -5
        existing_vote = next((x for x in self.votes if x.user.id == user.id), None)

        if existing_vote:
            db.session.delete(existing_vote)
        else:
            vote = Vote(
                type='post',
                contest=get_contest_name(),
                score=score,
                user=user
            )
            self.votes.append(vote)
        db.session.commit()

    @property
    def vote_score(self):
        return sum_of_votes(self.votes)
