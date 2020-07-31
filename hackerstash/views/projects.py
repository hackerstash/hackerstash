from flask import Blueprint, render_template, redirect, url_for, g, request
from hackerstash.db import db
from hackerstash.lib.images import upload_image, delete_image
from hackerstash.lib.invites import generate_invite_link
from hackerstash.lib.emails.factory import EmailFactory
from hackerstash.lib.notifications.factory import NotificationFactory
from hackerstash.models.user import User
from hackerstash.models.member import Member
from hackerstash.models.project import Project
from hackerstash.models.invite import Invite
from hackerstash.utils.auth import login_required, author_required, published_project_required

projects = Blueprint('projects', __name__)


@projects.route('/projects')
def index():
    all_projects = Project.query.filter_by(published=True)
    return render_template('projects/index.html', projects=all_projects)


@projects.route('/projects/<project_id>')
def show(project_id):
    project = Project.query.get(project_id)

    if not project:
        return render_template('projects/404.html')

    return render_template('projects/show.html', project=project)


@projects.route('/projects/create')
@login_required
def create():
    user = User.query.get(g.user.id)

    if user.member:
        return redirect(url_for('projects.show', project_id=user.member.project.id))

    project = Project(name='Untitled')
    member = Member(owner=True, user=user, project=project)

    db.session.add(project)
    db.session.add(member)
    db.session.commit()

    return redirect(url_for('projects.edit', project_id=project.id))


@projects.route('/projects/<project_id>/edit')
@login_required
@member_required
def edit(project_id):
    project = Project.query.get(project_id)
    return render_template('projects/edit.html', project=project)


@projects.route('/projects/<project_id>/update', methods=['POST'])
@login_required
@member_required
def update(project_id):
    project = Project.query.get(project_id)

    # Flask adds the empty file for some reason
    if 'file' in request.files and request.files['file'].filename != '':
        key = upload_image(request.files['file'])
        project.avatar = key
    elif 'avatar' in request.form and not request.form['avatar'] and project.avatar:
        delete_image(project.avatar)
        project.avatar = None

    for key, value in request.form.items():
        if key not in ['file', 'avatar']:
            setattr(project, key, value)

    lists = ['fundings', 'business_models', 'platforms_and_devices']

    for key in lists:
        val = request.form.getlist(key)
        if val:
            setattr(project, key, val)

    db.session.commit()
    return redirect(url_for('projects.show', project_id=project.id))


@projects.route('/projects/<project_id>/delete')
@login_required
@member_required
def destroy(project_id):
    project = Project.query.get(project_id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('projects.index'))


@projects.route('/projects/<project_id>/members/add')
@login_required
@member_required
def add_members(project_id):
    project = Project.query.get(project_id)
    return render_template('projects/members/add.html', project=project)


@projects.route('/projects/<project_id>/members/create', methods=['POST'])
@login_required
@member_required
def invite_member(project_id):
    email = request.form['email']
    link = generate_invite_link(email)
    user = User.query.filter_by(email=email).first()
    project = Project.query.get(project_id)
    is_already_member = user and user.member

    if not project.has_member_with_email(email) and not is_already_member:
        invite = Invite(
            email=email,
            first_name=request.form['first_name'],
            role=request.form['role'],
            link=link,
            project=project
        )
        db.session.add(invite)
        db.session.commit()

        if user:
            NotificationFactory.create('MEMBER_INVITED', {'invite': invite, 'user': user}).publish()
        else:
            EmailFactory.create('INVITE_TO_PROJECT', email, {'invite': invite}).send()

    return redirect(url_for('projects.edit', project_id=project.id, tab='2'))


@projects.route('/projects/<project_id>/members/<invite_id>/delete')
@login_required
@member_required
def remove_invite(project_id, invite_id):
    invite = Invite.query.get(invite_id)
    db.session.delete(invite)
    db.session.commit()
    return redirect(url_for('projects.edit', project_id=project_id, tab='2'))


@projects.route('/projects/<project_id>/publish', methods=['POST'])
@login_required
@member_required
def publish(project_id):
    project = Project.query.get(project_id)

    project.published = True
    db.session.commit()

    return redirect(url_for('projects.show', project_id=project.id))


@projects.route('/projects/<project_id>/unpublish')
@login_required
@member_required
def unpublish(project_id):
    project = Project.query.get(project_id)

    project.published = False
    db.session.commit()

    return redirect(url_for('projects.show', project_id=project.id))


@projects.route('/projects/<project_id>/vote')
@login_required
@published_project_required
def vote_project(project_id):
    project = Project.query.get(project_id)

    if project.id != g.user.member.project.id:
        project.vote(g.user, request.args.get('direction', 'up'))

    return redirect(url_for('projects.show', project_id=project.id))
