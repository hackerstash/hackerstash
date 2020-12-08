from hackerstash.lib.logging import Logging
from hackerstash.lib.emails.factory import email_factory
from hackerstash.lib.webhooks.base import Base
from hackerstash.models.project import Project

log = Logging(module='Webhook::GoalSetting')


class GoalSetting(Base):
    # The permitted list of hours
    time_remaining = [48, 24, 8, 1]

    def __init__(self, payload: dict) -> None:
        """
        Initialise an instance of the GoalSetting class
        :param payload: dict
        """
        super().__init__(payload)

        time_remaining = payload.get('time_remaining')

        log.info('Preparing email', {'time_remaining': time_remaining})

        if time_remaining not in self.time_remaining:
            raise Exception(f'{time_remaining} is not valid')

        for project in Project.query.all():
            if not project.active_goals:
                for member in project.members:
                    payload = {
                        'time_remaining': time_remaining,
                        'member': member
                    }
                    email_factory('goal_setting', member.user.email, payload).send()
