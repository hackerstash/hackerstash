from hackerstash.lib.notifications.base import Base


class MemberVerified(Base):
    def __init__(self, payload: dict) -> None:
        """
        Initialise an instance of the MemberVerified class
        :param payload: dict
        """
        super().__init__(payload)

        member = payload['member']

        for m in member.project.members:
            if m.id != member.id:
                self.notifications_to_send.append({
                    'user': m.user,
                    'payload': payload,
                    'email_type': 'member_joined_project',
                    'notification_type': 'a_team_member_joined_your_project',
                    'notification_message': self.render_notification_message('a_team_member_joined_your_project')
                })
