from flask import g
from hackerstash.lib.challenges.base import Base
from hackerstash.lib.logging import Logging

log = Logging(module='Challenges::PostCreated')


class PostCreated(Base):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)

        project = g.user.project

        if not self.has_completed(project, 'published_a_post'):
            log.info('Incrementing challenge', {'type': 'published_a_post', 'project_id': project.id})
            project.create_or_inc_challenge('published_a_post')
