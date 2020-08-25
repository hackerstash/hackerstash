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
            if not self.has_completed(user.member.project, 'comment_on_a_competitors_post'):
                logging.info(f'Awarding \'comment_on_a_competitors_post\' challenge for \'{project.id}\'')
                project.create_or_inc_challenge('comment_on_a_competitors_post')

            if not self.has_completed(user.member.project, 'comment_on_five_competitors_posts'):
                logging.info(f'Awarding \'comment_on_five_competitors_posts\' challenge for \'{project.id}\'')
                project.create_or_inc_challenge('comment_on_five_competitors_posts')
