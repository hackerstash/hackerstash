from hackerstash.lib.notifications.base import Base


class FollowerCreated(Base):
    def __init__(self, payload):
        super().__init__(payload)

        user = payload['user']

        self.notifications_to_send.append({
            # TODO
            'email': user.email,
            'email_type': 'NEW_FOLLOWER',
            'notification_type': 'you_have_a_new_follower'
        })