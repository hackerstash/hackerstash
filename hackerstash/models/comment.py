from hackerstash.db import db
from hackerstash.models.vote import Vote
from hackerstash.utils.contests import get_contest_name
from hackerstash.utils.votes import sum_of_votes

votes = db.Table(
    'comments_votes',
    db.Column('vote_id', db.Integer, db.ForeignKey('votes.id'), primary_key=True),
    db.Column('comment_id', db.Integer, db.ForeignKey('comments.id'), primary_key=True)
)


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)

    body = db.Column(db.String)
    parent_comment_id = db.Column(db.Integer)

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    votes = db.relationship('Vote', secondary=votes, lazy='subquery', backref=db.backref('comment', lazy=True))

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        return f'<Comment {self.id}>'

    def vote(self, user, direction):
        score = 1 if direction == 'up' else -1
        existing_vote = next((x for x in self.votes if x.user.id == user.id), None)

        if existing_vote:
            self.votes.remove(existing_vote)
        else:
            vote = Vote(
                type='comment',
                contest=get_contest_name(),
                score=score,
                user=user
            )
            self.votes.append(vote)
        db.session.commit()

    @property
    def vote_score(self):
        return sum_of_votes(self.votes)
