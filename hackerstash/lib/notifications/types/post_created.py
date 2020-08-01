from hackerstash.lib.notifications.base import Base


class PostCreated(Base):
    def __init__(self, payload):
        super().__init__(payload)

        post = payload['post']

        for follower in post.user.followers:
            self.notifications_to_send.append({
                # TODO
                'email': follower.email,
                'email_type': 'FOLLOWER_CREATED_POST',
                'notification_type': 'a_follower_posts_an_update'
            })
