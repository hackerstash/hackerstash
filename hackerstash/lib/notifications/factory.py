from typing import Union
from hackerstash.lib.notifications.types.comment_created import CommentCreated
from hackerstash.lib.notifications.types.comment_voted import CommentVoted
from hackerstash.lib.notifications.types.follower_created import FollowerCreated
from hackerstash.lib.notifications.types.member_invited import MemberInvited
from hackerstash.lib.notifications.types.member_removed import MemberRemoved
from hackerstash.lib.notifications.types.member_verified import MemberVerified
from hackerstash.lib.notifications.types.mention_created import MentionCreated
from hackerstash.lib.notifications.types.post_created import PostCreated
from hackerstash.lib.notifications.types.post_voted import PostVoted
from hackerstash.lib.notifications.types.prize_awarded import PrizeAwarded
from hackerstash.lib.notifications.types.project_vote_reminder import ProjectVoteReminder

notification_factory_response = Union[
    CommentCreated,
    CommentVoted,
    FollowerCreated,
    MemberInvited,
    MemberRemoved,
    MemberVerified,
    MentionCreated,
    PostCreated,
    PostVoted,
    PrizeAwarded,
    ProjectVoteReminder
]


def notification_factory(notification_type: str, payload: dict) -> notification_factory_response:
    """
    Process a notification event
    :param notification_type: str
    :param payload: dict
    :return: notification_factory_response
    """
    if notification_type == 'comment_created':
        return CommentCreated(payload)
    if notification_type == 'comment_voted':
        return CommentVoted(payload)
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
    if notification_type == 'prize_awarded':
        return PrizeAwarded(payload)
    if notification_type == 'project_vote_reminder':
        return ProjectVoteReminder(payload)

    raise Exception(f'{notification_type} is not a valid notification type')
