from hackerstash.lib.notifications.base import Base


def get_notification_type(direction):
    if direction == 'up':
        return 'someone_upvotes_your_post'
    else:
        return 'someone_downvotes_your_post'


class PostVoted(Base):
    def __init__(self, payload):
        super().__init__(payload)

        post = payload['post']
        direction = payload['direction']

        self.notifications_to_send.append({
            'user': post.user,
            'payload': payload,
            'email_type': 'VOTED_ON_POST',
            'notification_type': get_notification_type(direction),
            'notification_message': self.render_notification_message('someone_voted_your_post')
        })
