from hackerstash.lib.notifications.base import Base


class CommentVoted(Base):
    def __init__(self, payload):
        super().__init__(payload)

        comment = payload['comment']
        direction = payload['direction']

        self.notifications_to_send.append({
            # TODO
            'email': comment.user.email,
            'email_type': 'VOTED_ON_COMMENT',
            'notification_type': self.get_notification_type(direction)
        })

    def get_notification_type(self, direction):
        if direction == 'up':
            return 'someone_upvotes_your_comment'
        else:
            return 'someone_downvotes_your_comment'