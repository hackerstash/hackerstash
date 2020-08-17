from flask import g
from hackerstash.lib.challenges.base import Base
from hackerstash.models.challenge import Challenge


class PostCreated(Base):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)

        user = g.user

        # TODO not existing
        challenge = Challenge(
            key='post_created',
            year=self.year,
            week=self.week,
            project=user.member.project
        )
        self.challenges_to_create.append(challenge)

        # TODO post_streak
