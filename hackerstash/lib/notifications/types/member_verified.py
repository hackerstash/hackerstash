from hackerstash.lib.notifications.base import Base


class MemberVerified(Base):
    def __init__(self, payload):
        super().__init__(payload)

        member = payload['member']

        for m in member.project.members:
            if m.id != member.id:
                self.notifications_to_send.append({
                    # TODO
                    'email': m.user.email,
                    'email_type': 'MEMBER_JOINED_PROJECT',
                    'notification_type': 'a_team_member_joined_your_project'
                })
