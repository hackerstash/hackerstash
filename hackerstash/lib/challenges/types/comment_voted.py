from flask import g
from hackerstash.lib.challenges.base import Base
from hackerstash.models.challenge import Challenge


class CommentVoted(Base):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)

        user = g.user
        comment = payload['comment']

        if user.member.project.id != comment.user.member.project.id:
            # TODO not existing
            challenge = Challenge(
                key='received_comment_vote',
                week=self.week,
                year=self.year,
                project=comment.user.member.project
            )
            self.challenges_to_create.append(challenge)
