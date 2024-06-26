from hackerstash.lib.notifications.base import Base


class MemberInvited(Base):
    def __init__(self, payload: dict) -> None:
        """
        Initialise an instance of the MemberInvited class
        :param payload: dict
        """
        super().__init__(payload)

        user = payload['user']

        self.notifications_to_send.append({
            'user': user,
            'payload': payload,
            'email_type': 'invite_to_project',
            'notification_type': 'you_were_invited_to_join_a_project',
            'notification_message': self.render_notification_message('you_were_invited_to_join_a_project')
        })
