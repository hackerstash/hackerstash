from flask import Blueprint, render_template, g, request, redirect, url_for
from hackerstash.db import db
from hackerstash.models.user import User
from hackerstash.models.notification import Notification
from hackerstash.utils.auth import login_required

notifications = Blueprint('notifications', __name__)


@notifications.route('/notifications')
@login_required
def index():
    all_notifications = g.user.notifications
    read_notifications = list(filter(lambda x: not x.read, all_notifications))
    return render_template('notifications/index.html', notifications=read_notifications)


@notifications.route('/notifications/settings')
@login_required
def settings():
    return render_template('notifications/settings/index.html')


@notifications.route('/notifications/update', methods=['POST'])
@login_required
def update():
    user = User.query.get(g.user.id)

    for key, value in request.form.items():
        setattr(user.notifications_settings, key, value == 'true')

    db.session.commit()
    return redirect(url_for('notifications.index'))


@notifications.route('/notifications/mark_as_read')
@login_required
def mark_as_read():
    user = User.query.get(g.user.id)
    mark_all = request.args.get('all')
    now = db.func.now()

    if mark_all:
        for notification in user.notifications:
            notification.read = True
            notification.read_at = now
    else:
        notification_id = request.args.get('notification_id')
        notification = Notification.query.get(notification_id)
        notification.read = True
        notification.read_at = now

    db.session.commit()

    return redirect(url_for('notifications.index'))
