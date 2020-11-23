from hackerstash.lib.logging import Logging
from hackerstash.lib.webhooks.base import Base
from hackerstash.lib.notifications.factory import notification_factory
from hackerstash.models.challenge import Challenge
from hackerstash.models.project import Project

log = Logging(module='Webhook::ProjectVoteReminder')


class ProjectVoteReminder(Base):
    def __init__(self, payload: dict) -> None:
        """
        Initialise an instance of the ProjectVoteReminder class
        :param payload: dict
        """
        super().__init__(payload)

        log.info('Queuing up project vote reminders')
        projects = Project.query.filter_by(published=True)

        for project in projects:
            challenge = Challenge.get_by_key_and_week(project, 'award_ponts_to_three_projects')
            complete = challenge.complete if challenge else False

            if complete:
                log.info(f'Challenge is already complete', {'project_id': project.id})
            else:
                for member in project.members:
                    notification_factory('project_vote_reminder', {'user': member.user}).publish()
