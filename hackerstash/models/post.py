import re
from random import randint
from flask import g, request
from sqlalchemy import func, select, or_
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.hybrid import hybrid_property
from hackerstash.db import db
from hackerstash.lib.leaderboard import Leaderboard
from hackerstash.models.tag import Tag
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
    poll = db.relationship('Poll', backref='post', cascade='all,delete', lazy='joined', uselist=False)

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
        """
        Get the sum of all the votes
        :return: int
        """
        return sum(vote.score for vote in self.votes)

    @vote_score.expression
    def vote_score(cls):
        """
        SQL Expression for calculating the vote score
        :return: int
        """
        return select([func.sum(Vote.score)]).where(Vote.post_id == cls.id).label('vote_score')

    @property
    def day(self) -> int:
        """
        Return the day the post was created at
        :return: int
        """
        # Returns day of the week (1-7)
        return self.created_at.isocalendar()[2]

    @property
    def week(self) -> int:
        """
        Return the week the post was created at
        :return: int
        """
        return self.created_at.isocalendar()[1]

    @property
    def year(self) -> int:
        """
        Return the year the post was created at
        :return: int
        """
        return self.created_at.year

    @classmethod
    def following(cls):
        """
        Return a paginated set of posts that are authored
        by users that the current user follows, or belong to
        groups that the user follows
        :return:
        """
        page = request.args.get('page', 1, type=int)
        following_ids = [x.id for x in g.user.following]
        return cls.query\
            .options(joinedload(Post.user))\
            .filter(or_(Post.user_id.in_(following_ids), Post.tag_id.in_(g.user.group_ids))) \
            .order_by(Post.created_at.desc()) \
            .paginate(page, 25, False)

    @classmethod
    def newest(cls):
        """
        Return a paginated set of posts that are orederd by
        their created date
        :return:
        """
        page = request.args.get('page', 1, type=int)
        return cls.query\
            .options(joinedload(Post.user))\
            .order_by(Post.created_at.desc())\
            .paginate(page, 25, False)

    @classmethod
    def top(cls):
        """
        Return a paginated set of posts that are orederd by
        the posts vote score
        :return:
        """
        page = request.args.get('page', 1, type=int)
        return cls.query\
            .options(joinedload(Post.user))\
            .order_by(Post.vote_score == 0, Post.vote_score.desc())\
            .paginate(page, 25, False)

    @classmethod
    def groups(cls) -> [(Tag, list)]:
        """
        Return a list of all groups
        :return:
        """
        # Return the list of groups in a tuple
        return db.session\
            .query(Tag, func.count(Post.id))\
            .join(Tag)\
            .group_by(Tag)\
            .order_by(Tag.name.asc())\
            .all()

    def has_author(self, user) -> bool:
        """
        Return whether or not the user is the author of the post
        :param user: User
        :return: bool
        """
        return self.user.id == user.id if user else False

    def get_existing_vote_for_user(self, user) -> Vote:
        """
        Work out if someone in the users project has already
        voted for this post
        :param user: User
        :return: Vote
        """
        # Although a user clicked on the button, the
        # vote is actually made on behalf of the project
        # to stop people from creating 30 fake users and
        # downvote bombing other users
        return find_in_list(self.votes, lambda x: x.user.project.id == user.project.id)

    def vote_status(self, user):
        """
        Get the set of class names that should be used
        for the vote badges
        :param user: User
        :return: str
        """
        if not user:
            return 'disabled logged-out'
        if not user.member or not user.project.published:
            return 'disabled not-published'
        if self.project.id == user.project.id:
            return 'disabled own-project'

        existing_vote = self.get_existing_vote_for_user(user)
        return ('upvoted' if existing_vote.score > 0 else 'downvoted') if existing_vote else ''

    def vote(self, user, direction: str) -> None:
        """
        Vote on a post
        :param user: User
        :param direction: str
        :return: None
        """
        # Posts have a score of 5 points
        score = 5 if direction == 'up' else -5
        existing_vote = self.get_existing_vote_for_user(user)
        # Update the leaderboard
        Leaderboard(self.project).update(score)

        if existing_vote:
            db.session.delete(existing_vote)
        else:
            vote = Vote(type='post', score=score, user=user)
            self.votes.append(vote)
        db.session.commit()

    @classmethod
    def generate_url_slug(cls, title: str) -> str:
        """
        Generate a url slug for the post that will be used for
        SEO friendly urls
        :param title: str
        :return: str
        """
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

    @property
    def contains_code(self) -> bool:
        """
        Return whether or not the post contains a code block
        :return: bool
        """
        return '</pre>' in self.body
