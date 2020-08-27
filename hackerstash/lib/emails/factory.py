from hackerstash.lib.emails.types.close_account import CloseAccount
from hackerstash.lib.emails.types.commented_on_post import CommentedOnPost
from hackerstash.lib.emails.types.contact import Contact
from hackerstash.lib.emails.types.follower_created_post import FollowerCreatedPost
from hackerstash.lib.emails.types.login_token import LoginToken
from hackerstash.lib.emails.types.member_joined_project import MemberJoinedProject
from hackerstash.lib.emails.types.member_left_project import MemberLeftProject
from hackerstash.lib.emails.types.mentioned_in_comment import MentionedInComment
from hackerstash.lib.emails.types.mentioned_in_post import MentionedInPost
from hackerstash.lib.emails.types.new_follower import NewFollower
from hackerstash.lib.emails.types.removed_from_project import RemovedFromProject
from hackerstash.lib.emails.types.replied_to_comment import RepliedToComment
from hackerstash.lib.emails.types.signup_token import SignupToken
from hackerstash.lib.emails.types.voted_on_comment import VotedOnComment
from hackerstash.lib.emails.types.voted_on_post import VotedOnPost
from hackerstash.lib.emails.types.invite_to_project import InviteToProject
from hackerstash.lib.emails.types.waitlist_confirmation import WaitlistConfirmation


def email_factory(email_type, email, payload):
    if email_type == 'close_account':
        return CloseAccount(email, payload)
    if email_type == 'commented_on_post':
        return CommentedOnPost(email, payload)
    if email_type == 'contact':
        return Contact(email, payload)
    if email_type == 'follower_created_post':
        return FollowerCreatedPost(email, payload)
    if email_type == 'login_token':
        return LoginToken(email, payload)
    if email_type == 'member_joined_project':
        return MemberJoinedProject(email, payload)
    if email_type == 'member_left_project':
        return MemberLeftProject(email, payload)
    if email_type == 'mentioned_in_comment':
        return MentionedInComment(email, payload)
    if email_type == 'mentioned_in_post':
        return MentionedInPost(email, payload)
    if email_type == 'new_follower':
        return NewFollower(email, payload)
    if email_type == 'removed_from_project':
        return RemovedFromProject(email, payload)
    if email_type == 'replied_to_comment':
        return RepliedToComment(email, payload)
    if email_type == 'signup_token':
        return SignupToken(email, payload)
    if email_type == 'invite_to_project':
        return InviteToProject(email, payload)
    if email_type == 'voted_on_comment':
        return VotedOnComment(email, payload)
    if email_type == 'voted_on_post':
        return VotedOnPost(email, payload)
    if email_type == 'waitlist_confirmation':
        return WaitlistConfirmation(email, payload)

    raise Exception(f'{email_type} is not a valid email type')
