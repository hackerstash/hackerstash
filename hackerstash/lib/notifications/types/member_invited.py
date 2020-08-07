from hackerstash.lib.notifications.base import Base


class MemberInvited(Base):
    def __init__(self, payload):
        super().__init__(payload)

        user = payload['user']

        self.notifications_to_send.append({
            'user': user,
            'payload': payload,
            'email_type': 'invited_to_project',
            'notification_type': 'you_were_invited_to_join_a_project',
            'notification_message': self.render_notification_message('you_were_invited_to_join_a_project')
        })
