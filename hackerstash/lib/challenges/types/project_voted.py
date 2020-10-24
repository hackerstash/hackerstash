from flask import g
from hackerstash.lib.challenges.base import Base
from hackerstash.lib.logging import Logging

log = Logging(module='Challenges::ProjectVoted')


class ProjectVoted(Base):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)

        user = g.user

        if not self.has_completed(user.project, 'award_ponts_to_three_projects'):
            log.info('Incrementing challenge', {'type': 'award_ponts_to_three_projects', 'project_id': user.project.id})
            user.project.create_or_inc_challenge('award_ponts_to_three_projects')
