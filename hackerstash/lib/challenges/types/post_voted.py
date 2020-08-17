from flask import g
from hackerstash.lib.challenges.base import Base
from hackerstash.models.challenge import Challenge


class PostVoted(Base):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)

        user = g.user
        post = payload['post']

        if user.member.project.id != post.project.id:
            # TODO not existing
            challenge = Challenge(
                key='given_post_vote',
                week=self.week,
                year=self.year,
                project=user.member.project
            )
            self.challenges_to_create.append(challenge)

            # TODO not existing
            challenge = Challenge(
                key='received_post_vote',
                week=self.week,
                year=self.year,
                project=post.project
            )
            self.challenges_to_create.append(challenge)

            # TODO not existing
            challenge = Challenge(
                key='award_points',
                week=self.week,
                year=self.year,
                project=user.member.project
            )
            self.challenges_to_create.append(challenge)
