from flask import g
from hackerstash.lib.challenges.base import Base
from hackerstash.lib.logging import logging


def is_not_members_comment(user, comment):
    return user.member.project.id != comment.post.project.id


class CommentCreated(Base):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)

        user = g.user
        project = user.member.project
        comment = payload['comment']

        if is_not_members_comment(user, comment):
            if not self.has_completed(user.member.project.challenges, 'comment_created'):
                logging.info(f'Awarding 5 points to "{project.id}" for "comment_created"')
                project.create_or_inc_challenge('comment_created')
