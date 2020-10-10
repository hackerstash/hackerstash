import re
from random import randint
from flask import g, request
from sqlalchemy import func, select
from sqlalchemy.ext.hybrid import hybrid_property
from hackerstash.db import db
from hackerstash.models.vote import Vote
from hackerstash.utils.helpers import find_in_list


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    url_slug = db.Column(db.String, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))
    comments = db.relationship('Comment', backref='post', cascade='all,delete', lazy='joined', order_by='Comment.created_at.desc()')
    votes = db.relationship('Vote', backref='post', cascade='all,delete', lazy='joined')

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self) -> str:
        return f'<Post {self.title[:30]}...>'

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

    @property
    def day(self):
        # Returns day of the week (1-7)
        return self.created_at.isocalendar()[2]

    @property
    def week(self):
        return self.created_at.isocalendar()[1]

    @property
    def year(self):
        return self.created_at.year

    @classmethod
    def following(cls):
        # Return a paginated set of posts that are authored
        # by users that the current user follows
        page = request.args.get('page', 1, type=int)
        following_ids = [x.id for x in g.user.following]
        return cls.query.filter(Post.user_id.in_(following_ids)).paginate(page, 25, False)

    @classmethod
    def newest(cls):
        # Return a paginated set of posts that are orederd by
        # their created date
        page = request.args.get('page', 1, type=int)
        return cls.query.order_by(Post.created_at.desc()).paginate(page, 25, False)

    @classmethod
    def top(cls):
        # Return a paginated set of posts that are orederd by
        # the posts vote score
        page = request.args.get('page', 1, type=int)
        return cls.query.order_by(Post.vote_score == 0, Post.vote_score.desc()).paginate(page, 25, False)

    def has_author(self, user):
        return self.user.id == user.id if user else False

    def get_existing_vote_for_user(self, user):
        # Although a user clicked on the button, the
        # vote is actually made on behalf of the project
        # to stop people from creating 30 fake users and
        # downvote bombing other users
        return find_in_list(self.votes, lambda x: x.user.member.project.id == user.member.project.id)

    def vote_status(self, user):
        if not user:
            return 'disabled logged-out'
        if user.member and self.project.ghost:
            return 'disabled ghost'
        if not user.member or not user.member.project.published:
            return 'disabled not-published'
        if self.project.id == user.member.project.id:
            return 'disabled own-project'
        if self.project.ghost:
            return 'disabled ghost'

        existing_vote = self.get_existing_vote_for_user(user)
        return ('upvoted' if existing_vote.score > 0 else 'downvoted') if existing_vote else ''

    def vote(self, user, direction: str) -> None:
        # Posts have a score of 5 points
        score = 5 if direction == 'up' else -5
        existing_vote = self.get_existing_vote_for_user(user)

        if existing_vote:
            db.session.delete(existing_vote)
        else:
            vote = Vote(type='post', score=score, user=user)
            self.votes.append(vote)
        db.session.commit()

    @classmethod
    def generate_url_slug(cls, title: str) -> str:
        exists = cls.query.filter_by(url_slug=title).first()

        if exists:
            return title + f'-{randint(0, 10)}'

        # Replace all non a-z with hyphens, then
        # tidy up any double hyphens or trailing
        # hyphens.
        title = re.sub(r'([^a-zA-Z0-9])', '-', title)
        title = re.sub(r'(-{2,})', '-', title)
        title = re.sub(r'-$', '', title)
        title = re.sub(r'^-', '', title)
        return title.lower()
