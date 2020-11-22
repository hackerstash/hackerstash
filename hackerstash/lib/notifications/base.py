from flask import render_template
from hackerstash.db import db
from hackerstash.lib.logging import Logging
from hackerstash.lib.emails.factory import email_factory
from hackerstash.models.notification import Notification

log = Logging(module='Notifications')
base_template_path = 'partials/notifications/'


def notification_enabled(notification: dict, notification_type: str) -> bool:
    """
    Check whether a notification type is enabled
    :param notification: dict
    :param notification_type: str
    :return: bool
    """
    key = f'{notification["notification_type"]}_{notification_type}'
    return getattr(notification['user'].notifications_settings, key, False)


def create_web_notification(notification: dict) -> None:
    """
    Create a new notification
    :param notification: dict
    :return: None
    """
    notification = Notification(
        read=False,
        type=notification['notification_type'],
        user=notification['user'],
        message=notification['notification_message']
    )
    db.session.add(notification)
    db.session.commit()


def create_email_notification(notification: dict) -> None:
    """
    Create a new email notification
    :param notification: dict
    :return: None
    """
    email_factory(notification['email_type'], notification['user'].email, notification['payload']).send()


class Base:
    def __init__(self, payload: dict) -> None:
        """
        Initialise an instance of the Notification base class
        :param payload: dict
        """
        self.payload = payload
        self.notifications_to_send = []

    def publish(self) -> None:
        """
        Publish the notifications that have been created
        :return: None
        """
        notification_types = list(map(lambda x: x['notification_type'], self.notifications_to_send))
        log.info('Publishing notifications', {'types': notification_types})

        for notification in self.notifications_to_send:
            if notification_enabled(notification, 'web'):
                log.info(f'Creating web notification', {'user_id': notification['user'].id, 'type': notification['notification_type']})
                create_web_notification(notification)

            if notification_enabled(notification, 'email'):
                log.info(f'Creating email notification', {'user_id': notification['user'].id, 'type': notification['notification_type']})
                create_email_notification(notification)

    def render_notification_message(self, name: str) -> str:
        """
        Generate the message for the on site notification
        :param name: str
        :return: str
        """
        file = f'{base_template_path}{name}.html'
        return render_template(file, **self.payload)
