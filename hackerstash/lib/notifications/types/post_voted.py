from hackerstash.lib.notifications.base import Base


class PostVoted(Base):
    def __init__(self, payload):
        super().__init__(payload)

        post = payload['post']
        direction = payload['direction']

        self.notifications_to_send.append({
            # TODO
            'email': post.user.email,
            'email_type': 'VOTED_ON_POST',
            'notification_type': self.get_notification_type(direction)
        })

    def get_notification_type(self, direction):
        if direction == 'up':
            return 'someone_upvotes_your_post'
        else:
            return 'someone_downvotes_your_post'
