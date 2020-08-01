from hackerstash.lib.notifications.base import Base


class MemberRemoved(Base):
    def __init__(self, payload):
        super().__init__(payload)

        member = payload['member']

        for m in member.project.members:
            if m.id == member.id:
                self.notifications_to_send.append({
                    # TODO
                    'email': m.user.email,
                    'email_type': 'REMOVED_FROM_PROJECT',
                    'notification_type': 'you_were_removed_from_a_project'
                })
            else:
                self.notifications_to_send.append({
                    # TODO
                    'email': m.user.email,
                    'email_type': 'MEMBER_LEFT_PROJECT',
                    'notification_type': 'a_team_member_left_your_project'
                })
