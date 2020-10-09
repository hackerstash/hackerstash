from hackerstash.lib.logging import logging
from hackerstash.lib.webhooks.base import Base
from hackerstash.lib.notifications.factory import notification_factory
from hackerstash.models.challenge import Challenge
from hackerstash.models.contest import Project


class ProjectVoteReminder(Base):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)

        logging.info('Queuing up project vote reminders via webhook')
        projects = Project.query.filter_by(published=True)

        for project in projects:
            challenge = Challenge.get_by_key_and_week(project, 'award_ponts_to_three_projects')
            complete = challenge.complete if challenge else False

            if complete:
                logging.info(f'Challenge is already complete for \'{project.name}\', skipping...')
            else:
                for member in project.members:
                    notification_factory('project_vote_reminder', {'user': member.user}).publish()
