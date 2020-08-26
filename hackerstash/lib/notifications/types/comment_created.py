from flask import g
from hackerstash.lib.notifications.base import Base
from hackerstash.models.comment import Comment


class CommentCreated(Base):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)

        comment = payload['comment']

        # Don't notify yourself that you commented
        # on your own post
        if comment.post.user.id != g.user.id:
            # If the comment has no parent then the post author should
            # recieve a notification. Otherwise the owner of the parent
            # comment should receive it instead.
            if comment.parent_comment_id:
                parent_comment = Comment.query.get(comment.parent_comment_id)

                # Likewise, you don't want to know that
                # you replied to yourself
                if parent_comment.user.id != g.user.id:
                    self.notifications_to_send.append({
                        'user': parent_comment.user,
                        'payload': payload,
                        'email_type': 'replied_to_comment',
                        'notification_type': 'someone_replies_to_your_comment',
                        'notification_message': self.render_notification_message('someone_replies_to_your_comment')
                    })
            else:
                self.notifications_to_send.append({
                    'user': comment.post.user,
                    'payload': payload,
                    'email_type': 'commented_on_post',
                    'notification_type': 'someone_comments_on_your_post',
                    'notification_message': self.render_notification_message('someone_comments_on_your_post')
                })
