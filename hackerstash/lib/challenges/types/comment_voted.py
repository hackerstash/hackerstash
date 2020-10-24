from flask import g
from hackerstash.lib.challenges.base import Base
from hackerstash.lib.logging import Logging

log = Logging(module='Challenges::CommentVoted')


def is_not_members_comment(user, comment):
    return user.project.id != comment.user.project.id


class CommentVoted(Base):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)

        user = g.user
        comment = payload['comment']
        comment_project = comment.user.project

        if is_not_members_comment(user, comment):
            if not self.has_completed(comment_project, 'have_five_comments_upvoted'):
                log.info('Incrementing challenge', {'type': 'have_five_comments_upvoted', 'project_id': comment_project.id})
                comment.user.project.create_or_inc_challenge('have_five_comments_upvoted')
