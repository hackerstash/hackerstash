from flask import Blueprint, render_template, g, request, redirect, url_for, jsonify
from hackerstash.db import db
from hackerstash.lib.logging import Logging
from hackerstash.models.notification import Notification
from hackerstash.utils.auth import login_required

log = Logging(module='Views::Notifications')
notifications = Blueprint('notifications', __name__)


@notifications.route('/notifications')
@login_required
def index() -> str:
    all_notifications = g.user.notifications
    splits = {
        'all': all_notifications,
        'read': [x for x in all_notifications if x.read],
        'unread': [x for x in all_notifications if not x.read]
    }
    return render_template('notifications/index.html', notifications=splits)


@notifications.route('/notifications/settings')
@login_required
def settings() -> str:
    return render_template('notifications/settings/index.html')


@notifications.route('/notifications/update', methods=['POST'])
@login_required
def update() -> str:
    log.info('Updating notifications', {'user_id': g.user.id})

    for key, value in request.form.items():
        setattr(g.user.notifications_settings, key, value == 'true')

    db.session.commit()
    return redirect(url_for('notifications.index', saved=1))


@notifications.route('/notifications/mark_as_read')
@login_required
def mark_as_read() -> str:
    mark_all = request.args.get('all')
    now = db.func.now()

    log.info('Marking notifications as read', {'user_id': g.user.id, 'notification_data': request.form})

    if mark_all:
        for notification in g.user.notifications:
            notification.read = True
            notification.read_at = now
    else:
        notification_id = request.args.get('notification_id')
        notification = Notification.query.get(notification_id)
        notification.read = True
        notification.read_at = now

    db.session.commit()
    return redirect(url_for('notifications.index'))


@notifications.route('/notifications/delete')
@login_required
def delete() -> str:
    delete_all = request.args.get('all')

    log.info('Deleting notifications', {'user_id': g.user.id, 'notification_data': request.form})

    if delete_all:
        for notification in g.user.notifications:
            if notification.read:
                db.session.delete(notification)
    else:
        notification_id = request.args.get('notification_id')
        notification = Notification.query.get(notification_id)
        db.session.delete(notification)

    db.session.commit()
    return redirect(url_for('notifications.index'))


@notifications.route('/notifications/count')
@login_required
def notification_count():
    if request.headers.get('X-Requested-With') == 'fetch':
        all_notifications = g.user.notifications
        unread_notifications = list(filter(lambda x: not x.read, all_notifications))
        return jsonify({'count': len(unread_notifications)})
    else:
        # Not really sure what to do here, but it's
        # unlikely to happen.
        return redirect(url_for('notifications.index'))
