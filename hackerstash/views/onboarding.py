import re
import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, g
from hackerstash.db import db
from hackerstash.lib.images import Images
from hackerstash.lib.invites import Invites
from hackerstash.lib.logging import Logging
from hackerstash.models.user import User
from hackerstash.models.member import Member
from hackerstash.models.project import Project
from hackerstash.models.notification_setting import NotificationSetting
from hackerstash.utils.auth import login_required

log = Logging(module='Views::Onboarding')
onboarding = Blueprint('onboarding', __name__)


@onboarding.route('/onboarding')
def index() -> str:
    """
    Redirect to the correct tab based on their
    progress so far
    :return: str
    """
    user = g.user
    if not user.username:
        return redirect(url_for('onboarding.user_tab'))
    return redirect(url_for('onboarding.project_tab'))


@onboarding.route('/onboarding/user', methods=['GET', 'POST'])
@login_required
def user_tab() -> str:
    """
    Render or update the user onboarding tab
    :return: str
    """
    if request.method == 'GET':
        return render_template('onboarding/user/index.html')

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    username = re.sub(r'[^a-z0-9\_\-\.]+', '', request.form['username'], flags=re.IGNORECASE)

    user = User.query.get(session['id'])
    user.first_name = first_name
    user.last_name = last_name

    if not user.username and User.username_exists(username):
        log.info('Username is taken', {'username': username})
        flash('This username is already taken', 'failure')
        return redirect(url_for('onboarding.user'))

    if user.username != username:
        user.username = username
    if not user.notifications_settings:
        user.notifications_settings = NotificationSetting()

    # Flask adds the empty file for some reason
    if 'file' in request.files and request.files['file'].filename != '':
        key = Images.upload(request.files['file'])
        user.avatar = key

    db.session.commit()

    # If the user was invited but didn't have an
    # account, we can add them to the project now
    Invites.verify(user)
    return redirect(url_for('onboarding.project_tab'))


@onboarding.route('/onboarding/project', methods=['GET', 'POST'])
@login_required
def project_tab() -> str:
    """
    Render or update the project onboarding tab
    :return: str
    """
    if g.user.member:
        project = g.user.member.project
    else:
        now = datetime.datetime.now()
        project = Project(name='Untitled', time_commitment='FULL_TIME', start_month=now.month - 1, start_year=now.year)
        member = Member(owner=True, user=g.user, project=project)
        db.session.add(project)
        db.session.add(member)
        db.session.commit()

    if request.method == 'GET':
        return render_template('onboarding/project/index.html', project=project)

    # Flask adds the empty file for some reason
    if 'file' in request.files and request.files['file'].filename != '':
        key = Images.upload(request.files['file'])
        project.avatar = key
    elif 'avatar' in request.form and not request.form['avatar'] and project.avatar:
        Images.delete(project.avatar)
        project.avatar = None

    project.published = True

    for key, value in request.form.items():
        if key not in ['file', 'avatar']:
            # Rich text always uses body as the key
            key = 'description' if key == 'body' else key
            setattr(project, key, value)

    lists = ['fundings', 'business_models', 'platforms_and_devices']

    for key in lists:
        val = request.form.getlist(key)
        if val:
            setattr(project, key, val)

    db.session.commit()
    return redirect(url_for('projects.show', project_id=project.id))
