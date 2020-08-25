from flask import g
from hackerstash.lib.challenges.base import Base
from hackerstash.lib.logging import logging


def is_not_our_project(user, project):  # OUR PROJECT ☭
    return user.member.project.id != project.id


class ProjectVoted(Base):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)

        user = g.user
        project = payload['project']

        if is_not_our_project(user, project):
            if not self.has_completed(user.member.project, 'award_points_to_three_projects'):
                logging.info(f'Awarding \'given_project_vote\' challenge for \'{project.id}\'')
                user.member.project.create_or_inc_challenge('award_points_to_three_projects')

            if not self.has_completed(user.member.project, 'award_points_to_ten_projects'):
                logging.info(f'Awarding \'award_points_to_ten_projects\' challenge for \'{project.id}\'')
                user.member.project.create_or_inc_challenge('award_points_to_ten_projects')
