from hackerstash.lib.notifications.base import Base


class ProjectVoteReminder(Base):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)

        user = payload['user']

        self.notifications_to_send.append({
            'user': user,
            'payload': payload,
            'email_type': 'project_vote_reminder',
            'notification_type': 'project_vote_reminder',
            'notification_message': self.render_notification_message('project_vote_reminder')
        })
