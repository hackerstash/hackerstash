from flask import g
from hackerstash.lib.challenges.base import Base
from hackerstash.lib.logging import logging


class PostCreated(Base):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)

        project = g.user.member.project

        if not self.has_completed(project, 'published_a_post'):
            logging.info(f'Awarding "published_a_post" challenge for "{project.id}"')
            project.create_or_inc_challenge('published_a_post')

        # TODO
        # - five_day_post_streak
