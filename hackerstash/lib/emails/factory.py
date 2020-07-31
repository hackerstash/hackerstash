from hackerstash.lib.emails.types.close_account import CloseAccount
from hackerstash.lib.emails.types.commented_on_post import CommentedOnPost
from hackerstash.lib.emails.types.contact import Contact
from hackerstash.lib.emails.types.follower_created_post import FollowerCreatedPost
from hackerstash.lib.emails.types.login_token import LoginToken
from hackerstash.lib.emails.types.member_joined_project import MemberJoinedProject
from hackerstash.lib.emails.types.member_left_project import MemberLeftProject
from hackerstash.lib.emails.types.new_follower import NewFollower
from hackerstash.lib.emails.types.removed_from_project import RemovedFromProject
from hackerstash.lib.emails.types.replied_to_comment import RepliedToComment
from hackerstash.lib.emails.types.signup_token import SignupToken
from hackerstash.lib.emails.types.voted_on_comment import VotedOnComment
from hackerstash.lib.emails.types.voted_on_post import VotedOnPost
from hackerstash.lib.emails.types.invite_to_project import InviteToProject
from hackerstash.lib.emails.types.waitlist_confirmation import WaitlistConfirmation


class EmailFactory:
    @staticmethod
    def create(email_type, email, payload):
        if email_type == 'CLOSE_ACCOUNT':
            return CloseAccount(email, payload)
        if email_type == 'COMMENTED_ON_POST':
            return CommentedOnPost(email, payload)
        if email_type == 'CONTACT':
            return Contact(email, payload)
        if email_type == 'FOLLOWER_CREATED_POST':
            return FollowerCreatedPost(email, payload)
        if email_type == 'LOGIN_TOKEN':
            return LoginToken(email, payload)
        if email_type == 'MEMBER_JOINED_PROJECT':
            return MemberJoinedProject(email, payload)
        if email_type == 'MEMBER_LEFT_PROJECT':
            return MemberLeftProject(email, payload)
        if email_type == 'NEW_FOLLOWER':
            return NewFollower(email, payload)
        if email_type == 'REMOVED_FROM_PROJECT':
            return RemovedFromProject(email, payload)
        if email_type == 'REPLIED_TO_COMMENT':
            return RepliedToComment(email, payload)
        if email_type == 'SIGNUP_TOKEN':
            return SignupToken(email, payload)
        if email_type == 'INVITE_TO_PROJECT':
            return InviteToProject(email, payload)
        if email_type == 'VOTED_ON_COMMENT':
            return VotedOnComment(email, payload)
        if email_type == 'VOTED_ON_POST':
            return VotedOnPost(email, payload)
        if email_type == 'WAITLIST_CONFIRMATION':
            return WaitlistConfirmation(email, payload)

        raise Exception(f'{email_type} is not a valid email type')
