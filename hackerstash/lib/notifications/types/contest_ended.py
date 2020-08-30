from hackerstash.lib.notifications.base import Base


class ContestEnded(Base):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload)

        past_result = payload['past_result']

        if past_result.prize['value'] > 0:
            for member in past_result.project.members:
                self.notifications_to_send.append({
                    'user': member.user,
                    'payload': payload,
                    'email_type': 'prize_awarded',
                    'notification_type': 'prize_awarded',
                    'notification_message': self.render_notification_message('prize_awarded')
                })
