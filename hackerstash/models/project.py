import json
from flask import url_for
from sqlalchemy.types import ARRAY, JSON
from hackerstash.db import db
from hackerstash.lib.leaderboard import Leaderboard
from hackerstash.lib.logging import Logging
from hackerstash.lib.goals import Goals, GoalStates
from hackerstash.models.challenge import Challenge
from hackerstash.models.vote import Vote
from hackerstash.utils.helpers import find_in_list, html_to_plain_text

log = Logging(module='Models::Project')


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
    url = db.Column(db.String)
    description = db.Column(db.String)

    avatar = db.Column(db.String)
    banner = db.Column(db.String)

    location = db.Column(db.String)
    start_month = db.Column(db.Integer)
    start_year = db.Column(db.Integer)
    time_commitment = db.Column(db.String)
    team_size = db.Column(db.Integer)
    profile_button = db.Column(JSON(none_as_null=True))
    looking_for_cofounders = db.Column(db.Boolean)

    business_models = db.Column(ARRAY(db.String))
    fundings = db.Column(ARRAY(db.String))
    platforms_and_devices = db.Column(ARRAY(db.String))

    members = db.relationship('Member', backref='project', cascade='all,delete')
    invites = db.relationship('Invite', backref='project', cascade='all,delete')
    posts = db.relationship('Post', backref='project', cascade='all,delete')
    votes = db.relationship('Vote', backref='project', cascade='all,delete', lazy='joined')
    challenges = db.relationship('Challenge', backref='project', cascade='all,delete')
    reviews = db.relationship('Review', backref='project', cascade='all,delete')
    winners = db.relationship('Winner', backref='project', cascade='all,delete')
    goals = db.relationship('Goal', backref='project', cascade='all,delete', order_by='Goal.id.asc()')
    feedback = db.relationship('Feedback', backref='project', cascade='all,delete')

    ghost = db.Column(db.Boolean, default=False)
    published = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self) -> str:
        return f'<Project {self.name}>'

    def has_member(self, user) -> bool:
        """
        Return whether or not this user is a member of the project
        :param user: User
        :return: bool
        """
        member = self.get_member_by_id(user.id if user else None)
        return bool(member)

    def get_member_by_id(self, user_id=None):
        """
        Return the member of a project by using their id
        :param user_id: int
        :return: Member
        """
        return find_in_list(self.members, lambda x: x.user.id == user_id)

    def has_member_with_email(self, email: str):
        """
        Return the member of the project by their id
        :param email:
        :return: Member
        """
        return find_in_list(self.members, lambda x: x.user.email == email)

    def get_existing_vote_for_user(self, user) -> Vote:
        """
        Work out if someone in the users project has already
        voted for this project
        :param user: User
        :return: Vote
        """
        # Although a user clicked on the button, the
        # vote is actually made on behalf of the project
        # to stop people from creating 30 fake users and
        # downvote bombing other users
        return find_in_list(
            self.votes,
            # Projects are different as you can revote on them every month
            lambda x: x.user.project.id == user.project.id and x.is_current_contest
        )

    def vote(self, user, direction: str) -> None:
        """
        Vote on a project
        :param user: User
        :param direction: str
        :return: None
        """
        score = 10 if direction == 'up' else -10
        existing_vote = self.get_existing_vote_for_user(user)
        # Update the leaderboard
        Leaderboard(self).update(score)

        if existing_vote:
            db.session.delete(existing_vote)
        else:
            vote = Vote(type='project', score=score, user=user)
            self.votes.append(vote)
        db.session.commit()

    def vote_status(self, user) -> str:
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
        if self.id == user.project.id:
            return 'disabled own-project'

        existing_vote = self.get_existing_vote_for_user(user)
        return ('upvoted' if existing_vote.score > 0 else 'downvoted') if existing_vote else ''

    @property
    def plain_text_description(self) -> str:
        """
        Get the plain text description for the project
        :return: str
        """
        return html_to_plain_text(self.description, limit=240)

    @property
    def position(self) -> int:
        """
        Get the projects position on the leaderboard
        :return: int
        """
        if not self.published:
            return -1
        return Leaderboard(self).position

    @property
    def vote_score(self) -> int:
        """
        Get the projects vote score
        :return: int
        """
        return Leaderboard(self).score

    @property
    def all_votes(self) -> [Vote]:
        """
        Get all the votes for this project
        :return: [Vote]
        """
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
        """
        Return the sum of all the upvotes this project received
        :return: int
        """
        # Get all the votes for this contest that have a
        # positive score, therefore being an upvote
        votes = [vote for vote in self.all_votes if vote.is_current_contest and vote.score > 0]
        return len(votes)

    @property
    def downvotes(self) -> int:
        """
        Return the sum of all the downvotes this project received
        :return: int
        """
        # Get all the votes for this contest that have a
        # negative score, therefore being a downvote
        votes = [vote for vote in self.all_votes if vote.is_current_contest and vote.score < 0]
        return len(votes)

    @property
    def preview_json(self) -> str:
        """
        Get the json string for the project preview card
        :return: str
        """
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

    def create_or_inc_challenge(self, key: str) -> None:
        """
        Create or incremement a challenge
        :param key: str
        :return: None
        """
        challenge = Challenge.find_or_create(self, key)
        challenge.inc()
        db.session.commit()

    def create_or_set_challenge(self, key: str, value: int) -> None:
        """
        Create or set a challenge
        :param key: str
        :param value: int
        :return: None
        """
        challenge = Challenge.find_or_create(self, key)
        challenge.count = value
        db.session.commit()

    @property
    def number_of_completed_challenges(self) -> int:
        """
        Return the total number of completed challenges
        :return: int
        """
        completed = Challenge.get_completed_challenges_for_project(self)
        return len(completed)

    @property
    def active_goals(self) -> list:
        """
        Return the active goals for this week
        :return: [Goal]
        """
        return [goal for goal in self.goals if goal.current]

    @property
    def goal_status(self) -> GoalStates:
        """
        Return the enum for the current goal state
        :return: GoalStates
        """
        return Goals(self).status()

    @property
    def reviews_to_give(self) -> list:
        """
        Return which reviews this project needs to give this week
        :return: [Feedback]
        """
        current = [feedback for feedback in self.feedback if feedback.current]
        return sorted(current, key=lambda x: x.position, reverse=True)
