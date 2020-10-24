from sqlalchemy import func, select
from sqlalchemy.ext.hybrid import hybrid_property
from hackerstash.db import db
from hackerstash.models.vote import Vote
from hackerstash.utils.helpers import find_in_list


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)

    body = db.Column(db.String)
    parent_comment_id = db.Column(db.Integer)

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    votes = db.relationship('Vote', backref='comment', cascade='all,delete', lazy='joined')

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self) -> str:
        return f'<Comment {self.body[:30]}...>'

    # The default order should be newest first
    __mapper_args__ = {
        'order_by': created_at.desc()
    }

    @hybrid_property
    def vote_score(self):
        return sum(vote.score for vote in self.votes)

    @vote_score.expression
    def vote_score(cls):
        return select([func.sum(Vote.score)]).where(Vote.post_id == cls.id).label('vote_score')

    def get_existing_vote_for_user(self, user):
        # Although a user clicked on the button, the
        # vote is actually made on behalf of the project
        # to stop people from creating 30 fake users and
        # downvote bombing other users
        return find_in_list(self.votes, lambda x: x.user.project.id == user.project.id)

    def vote(self, user, direction: str) -> None:
        # Comments have a score of 1 point
        score = 1 if direction == 'up' else -1
        existing_vote = self.get_existing_vote_for_user(user)

        if existing_vote:
            db.session.delete(existing_vote)
        else:
            vote = Vote(type='comment', score=score, user=user)
            self.votes.append(vote)
        db.session.commit()

    def vote_status(self, user):
        if not user:
            return 'disabled logged-out'
        if not user.member or not user.project.published:
            return 'disabled not-published'
        if self.user.project.id == user.project.id:
            return 'disabled own-project'

        existing_vote = self.get_existing_vote_for_user(user)
        return ('upvoted' if existing_vote.score > 0 else 'downvoted') if existing_vote else ''
