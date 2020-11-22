from hackerstash.lib.notifications.base import Base


class FollowerCreated(Base):
    def __init__(self, payload: dict) -> None:
        """
        Initialise an instance of the FollowerCreated class
        :param payload: dict
        """
        super().__init__(payload)

        user = payload['user']

        self.notifications_to_send.append({
            'user': user,
            'payload': payload,
            'email_type': 'new_follower',
            'notification_type': 'you_have_a_new_follower',
            'notification_message': self.render_notification_message('you_have_a_new_follower')
        })
