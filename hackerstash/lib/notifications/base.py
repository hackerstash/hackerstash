from hackerstash.db import db
from hackerstash.lib.emails.factory import EmailFactory
from hackerstash.models.notification import Notification


def notification_enabled(notification, notification_type):
    key = f'{notification["notification_type"]}_{notification_type}'
    return getattr(notification['user'].notifications_settings, key, False)


def create_web_notification(notification):
    notification = Notification(
        read=False,
        type=notification['notification_type'],
        user=notification['user'],
        message=notification['notification_message']
    )
    db.session.add(notification)
    db.session.commit()


def create_email_notification(notification):
    EmailFactory.create(
        notification['email_type'],
        notification['user'].email,
        notification['payload']
    ).send()


class Base:
    def __init__(self, payload):
        self.payload = payload
        self.notifications_to_send = []

    def publish(self):
        print(f'Publishing notifications')

        for notification in self.notifications_to_send:
            if notification_enabled(notification, 'web'):
                print('Creating web notification')
                create_web_notification(notification)

            if notification_enabled(notification, 'email'):
                print('Creating email notification')
                create_email_notification(notification)
