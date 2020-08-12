from flask import g
from hackerstash.lib.challenges.base import Base
from hackerstash.models.challenge import Challenge


class PostCreated(Base):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)

        user = g.user
        post = payload['post']

        # publish_a_post
        challenge = Challenge(
            key='post_created',
            week=self.week,
            year=self.year,
            project=post.project
        )
        self.challenges_to_create.append(challenge)
