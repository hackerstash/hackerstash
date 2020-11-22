from flask import g
from hackerstash.lib.challenges.base import Base
from hackerstash.lib.logging import Logging

log = Logging(module='Challenges::CommentCreated')


def is_not_members_comment(user, comment) -> bool:
    """
    Return whether or not this user, or any member of this
    users project was the author
    :param user: User
    :param comment: Comment
    :return: bool
    """
    return user.project.id != comment.post.project.id


class CommentCreated(Base):
    def __init__(self, payload: dict) -> None:
        """
        Initialise an instance of the CommentCreated class
        :param payload: dict
        """
        super().__init__(payload)

        user = g.user
        project = user.project
        comment = payload['comment']

        if is_not_members_comment(user, comment):
            if not self.has_completed(user.project, 'comment_on_a_competitors_post'):
                log.info('Incrementing challenge', {'type': 'comment_on_a_competitors_post', 'project_id': project.id})
                project.create_or_inc_challenge('comment_on_a_competitors_post')

            if not self.has_completed(user.project, 'comment_on_five_competitors_posts'):
                log.info('Incrementing challenge', {'type': 'comment_on_five_competitors_posts', 'project_id': project.id})
                project.create_or_inc_challenge('comment_on_five_competitors_posts')
