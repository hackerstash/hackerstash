from hackerstash.lib.notifications.base import Base


class MemberRemoved(Base):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)

        member = payload['member']
        remover = payload['remover']

        for m in member.project.members:
            if m.user.id != remover.id:
                if m.id == member.id:
                    self.notifications_to_send.append({
                        'user': m.user,
                        'payload': payload,
                        'email_type': 'removed_from_project',
                        'notification_type': 'you_were_removed_from_a_project',
                        'notification_message': self.render_notification_message('you_were_removed_from_a_project')
                    })
                else:
                    self.notifications_to_send.append({
                        'user': m.user,
                        'payload': payload,
                        'email_type': 'member_left_project',
                        'notification_type': 'a_team_member_left_your_project',
                        'notification_message': self.render_notification_message('a_team_member_left_your_project')
                    })
