from flask import g
from hackerstash.lib.challenges.base import Base
from hackerstash.models.challenge import Challenge


class CommentCreated(Base):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)

        user = g.user
        comment = payload['comment']

        if user.member.project.id != comment.post.project.id:
            challenge = Challenge(
                key='comment_created',
                week=self.week,
                year=self.year,
                project=user.member.project
            )
            self.challenges_to_create.append(challenge)

