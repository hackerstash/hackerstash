from hackerstash.lib.notifications.base import Base


class MentionCreated(Base):
    def __init__(self, payload: dict) -> None:
        """
        Initialise an instance of the MentionCreated class
        :param payload: dict
        """
        super().__init__(payload)

        user = payload['user']
        post = payload.get('post')
        comment = payload.get('comment')

        # Don't send if they're mentioning themselves in their
        # own post
        if post and user.id != post.user.id:
            self.notifications_to_send.append({
                'user': user,
                'payload': payload,
                'email_type': 'mentioned_in_post',
                'notification_type': 'someone_mentions_you_in_post_or_comment',
                'notification_message': self.render_notification_message('someone_mentions_you_in_post')
            })

        # Don't send if they're mentioning themselves in their
        # own comment
        if comment and user.id != comment.user.id:
            self.notifications_to_send.append({
                'user': user,
                'payload': payload,
                'email_type': 'mentioned_in_comment',
                'notification_type': 'someone_mentions_you_in_post_or_comment',
                'notification_message': self.render_notification_message('someone_mentions_you_in_comment')
            })
