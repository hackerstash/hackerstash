from flask import g
from hackerstash.lib.challenges.base import Base
from hackerstash.lib.logging import logging


class ProjectVoted(Base):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)

        user = g.user

        if not self.has_completed(user.member.project, 'award_ponts_to_three_projects'):
            logging.info(f'Awarding \'award_ponts_to_three_projects\' challenge for \'{user.member.project.name}\'')
            user.member.project.create_or_inc_challenge('award_ponts_to_three_projects')
