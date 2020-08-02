from hackerstash.lib.emails.factory import EmailFactory


class Base:
    def __init__(self, payload):
        self.payload = payload
        self.notifications_to_send = []

    def publish(self):
        print(f'Publishing notifications')

        for notification in self.notifications_to_send:
            if self.notification_enabled(notification, 'web'):
                print('send web')
                pass
            if self.notification_enabled(notification, 'email'):
                EmailFactory.create(
                    notification['email_type'],
                    notification['user'].email,
                    notification['payload']
                ).send()

    def notification_enabled(self, notification, notification_type):
        key = f'{notification["notification_type"]}_{notification_type}'
        return getattr(notification['user'].notifications_settings, key, False)
