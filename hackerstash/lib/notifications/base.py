from flask import render_template
from hackerstash.db import db
from hackerstash.lib.logging import logging
from hackerstash.lib.emails.factory import email_factory
from hackerstash.models.notification import Notification

base_template_path = 'partials/notifications/'


def notification_enabled(notification, notification_type: str) -> bool:
    key = f'{notification["notification_type"]}_{notification_type}'
    return getattr(notification['user'].notifications_settings, key, False)


def create_web_notification(notification) -> None:
    notification = Notification(
        read=False,
        type=notification['notification_type'],
        user=notification['user'],
        message=notification['notification_message']
    )
    db.session.add(notification)
    db.session.commit()


def create_email_notification(notification) -> None:
    email_factory(notification['email_type'], notification['user'].email, notification['payload']).send()


class Base:
    def __init__(self, payload: dict) -> None:
        self.payload = payload
        self.notifications_to_send = []

    def publish(self) -> None:
        logging.info('Publishing notifications')

        for notification in self.notifications_to_send:
            if notification_enabled(notification, 'web'):
                logging.info('Creating web notification %s', notification)
                create_web_notification(notification)

            if notification_enabled(notification, 'email'):
                logging.info('Creating email notification %s', notification)
                create_email_notification(notification)

    def render_notification_message(self, name: str) -> str:
        file = f'{base_template_path}{name}.html'
        return render_template(file, **self.payload)
