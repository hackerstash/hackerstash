from hackerstash.lib.notifications.types.comment_created import CommentCreated
from hackerstash.lib.notifications.types.comment_voted import CommentVoted
from hackerstash.lib.notifications.types.contest_ended import ContestEnded
from hackerstash.lib.notifications.types.follower_created import FollowerCreated
from hackerstash.lib.notifications.types.member_invited import MemberInvited
from hackerstash.lib.notifications.types.member_removed import MemberRemoved
from hackerstash.lib.notifications.types.member_verified import MemberVerified
from hackerstash.lib.notifications.types.mention_created import MentionCreated
from hackerstash.lib.notifications.types.post_created import PostCreated
from hackerstash.lib.notifications.types.post_voted import PostVoted


def notification_factory(notification_type, payload):
    if notification_type == 'comment_created':
        return CommentCreated(payload)
    if notification_type == 'comment_voted':
        return CommentVoted(payload)
    if notification_type == 'contest_ended':
        return ContestEnded(payload)
    if notification_type == 'follower_created':
        return FollowerCreated(payload)
    if notification_type == 'member_invited':
        return MemberInvited(payload)
    if notification_type == 'member_removed':
        return MemberRemoved(payload)
    if notification_type == 'member_verified':
        return MemberVerified(payload)
    if notification_type == 'mention_created':
        return MentionCreated(payload)
    if notification_type == 'post_created':
        return PostCreated(payload)
    if notification_type == 'post_voted':
        return PostVoted(payload)

    raise Exception(f'{notification_type} is not a valid notification type')
