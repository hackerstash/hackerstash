from hackerstash.lib.notifications.base import Base


class PostCreated(Base):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)

        post = payload['post']

        for follower in post.user.followers:
            self.notifications_to_send.append({
                'user': follower,
                'payload': payload,
                'email_type': 'follower_created_post',
                'notification_type': 'a_follower_posts_an_update',
                'notification_message': self.render_notification_message('a_follower_posts_an_update')
            })
