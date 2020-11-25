from hackerstash.lib.notifications.base import Base


def get_notification_type(direction: str) -> str:
    """
    Get the correct notification type depending on whether
    the vote was up or down
    :param direction:
    :return: str
    """
    if direction == 'up':
        return 'someone_upvotes_your_comment'
    else:
        return 'someone_downvotes_your_comment'


class CommentVoted(Base):
    def __init__(self, payload: dict) -> None:
        """
        Initialise an instance of the CommentVoted class
        :param payload: dict
        """
        super().__init__(payload)

        comment = payload['comment']
        direction = payload['direction']

        self.notifications_to_send.append({
            'user': comment.user,
            'payload': payload,
            'email_type': 'voted_on_comment',
            'notification_type': get_notification_type(direction),
            'notification_message': self.render_notification_message('someone_voted_your_comment')
        })
