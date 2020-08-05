from flask import g
from hackerstash.lib.notifications.base import Base
from hackerstash.models.comment import Comment


class CommentCreated(Base):
    def __init__(self, payload):
        super().__init__(payload)

        comment = payload['comment']

        # Don't notify yourself that you commented
        # on your own post
        if comment.post.user.id != g.user.id:
            self.notifications_to_send.append({
                'user': comment.post.user,
                'payload': payload,
                'email_type': 'COMMENTED_ON_POST',
                'notification_type': 'someone_comments_on_your_post',
                'notification_message': self.render_notification_message('someone_comments_on_your_post')
            })

            if comment.parent_comment_id:
                parent_comment = Comment.query.get(comment.parent_comment_id)

                self.notifications_to_send.append({
                    'user': parent_comment.user,
                    'payload': payload,
                    'email_type': 'REPLIED_TO_COMMENT',
                    'notification_type': 'someone_replies_to_your_comment',
                    'notification_message': self.render_notification_message('someone_replies_to_your_comment')
                })
