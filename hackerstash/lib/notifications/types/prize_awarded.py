from hackerstash.lib.notifications.base import Base


class PrizeAwarded(Base):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)

        project = payload['project']

        for member in project.members:
            self.notifications_to_send.append({
                'user': member.user,
                'payload': payload,
                'email_type': 'prize_awarded',
                'notification_type': 'prize_awarded',
                'notification_message': self.render_notification_message('prize_awarded')
            })
