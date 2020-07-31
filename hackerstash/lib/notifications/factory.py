from hackerstash.lib.notifications.types.comment_created import CommentCreated
from hackerstash.lib.notifications.types.comment_voted import CommentVoted
from hackerstash.lib.notifications.types.follower_created import FollowerCreated
from hackerstash.lib.notifications.types.member_invited import MemberInvited
from hackerstash.lib.notifications.types.member_removed import MemberRemoved
from hackerstash.lib.notifications.types.member_verified import MemberVerified
from hackerstash.lib.notifications.types.post_created import PostCreated
from hackerstash.lib.notifications.types.post_voted import PostVoted


class NotificationFactory:
    @staticmethod
    def create(notification_type, payload):
        if notification_type == 'COMMENT_CREATED':
            return CommentCreated(payload)
        if notification_type == 'COMMENT_VOTED':
            return CommentVoted(payload)
        if notification_type == 'FOLLOWER_CREATED':
            return FollowerCreated(payload)
        if notification_type == 'MEMBER_INVITED':
            return MemberInvited(payload)
        if notification_type == 'MEMBER_REMOVED':
            return MemberRemoved(payload)
        if notification_type == 'MEMBER_VERIFIED':
            return MemberVerified(payload)
        if notification_type == 'POST_CREATED':
            return PostCreated(payload)
        if notification_type == 'POST_VOTED':
            return PostVoted(payload)

        raise Exception(f'{notification_type} is not a valid notification type')
