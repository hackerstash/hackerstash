from hackerstash.lib.notifications.base import Base


class MemberInvited(Base):
    def __init__(self, payload):
        super().__init__(payload)

        user = payload['user']
        invite = payload['invite']

        self.notifications_to_send.append({
            # TODO
            'email': invite.email,
            'email_type': 'INVITE_TO_PROJECT',
            'notification_type': 'you_were_invited_to_join_a_project'
        })
