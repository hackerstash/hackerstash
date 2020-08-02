from hackerstash.config import config
from hackerstash.lib.notifications.base import Base


class FollowerCreated(Base):
    def __init__(self, payload):
        super().__init__(payload)

        user = payload['user']

        self.notifications_to_send.append({
            'user': user,
            'payload': {
                **payload,
                'config': config
            },
            'email_type': 'NEW_FOLLOWER',
            'notification_type': 'you_have_a_new_follower'
        })
