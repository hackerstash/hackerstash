from hackerstash.db import db
from hackerstash.models.vote import Vote
from hackerstash.utils.helpers import find_in_list
from hackerstash.utils.votes import sum_of_votes


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

    def get_existing_vote_for_user(self, user):
        # Although a user clicked on the button, the
        # vote is actually made on behalf of the project
        # to stop people from creating 30 fake users and
        # downvote bombing other users
        return find_in_list(self.votes, lambda x: x.user.member.project.id == user.member.project.id)

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
        if not user.member or not user.member.project.published:
            return 'disabled not-published'
        if self.user.member.project.id == user.member.project.id:
            return 'disabled own-project'

        existing_vote = self.get_existing_vote_for_user(user)
        return 'upvoted' if existing_vote and existing_vote.score > 0 else 'downvoted'

    @property
    def vote_score(self) -> int:
        # Comments should show the votes for all time. Only
        # votes made this week will actually be taken into
        # account at the end of the tournament
        return sum_of_votes(self.votes, this_contest_only=False)
