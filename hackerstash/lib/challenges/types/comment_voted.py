from flask import g
from hackerstash.lib.challenges.base import Base
from hackerstash.lib.logging import logging


def is_not_members_comment(user, comment):
    return user.member.project.id != comment.user.member.project.id


class CommentVoted(Base):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)

        user = g.user
        comment = payload['comment']
        comment_project = comment.user.member.project

        if is_not_members_comment(user, comment):
            if not self.has_completed(comment_project, 'have_five_comments_upvoted'):
                logging.info(f'Awarding \'have_five_comments_upvoted\' challenge for \'{comment_project.name}\'')
                comment.user.member.project.create_or_inc_challenge('have_five_comments_upvoted')
