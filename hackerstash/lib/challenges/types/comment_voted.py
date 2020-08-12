from flask import g
from hackerstash.lib.challenges.base import Base
from hackerstash.models.challenge import Challenge


class CommentVoted(Base):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)

        user = g.user
        comment = payload['comment']

        pass
