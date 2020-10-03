import datetime
from flask import Blueprint, render_template, redirect, url_for, g, request, flash, get_template_attribute
from hackerstash.db import db
from hackerstash.lib.images import Images
from hackerstash.lib.invites import Invites
from hackerstash.lib.emails.factory import email_factory
from hackerstash.lib.logging import logging
from hackerstash.lib.notifications.factory import notification_factory
from hackerstash.lib.pagination import paginate
from hackerstash.lib.project_filtering import project_filtering
from hackerstash.lib.stripe import get_payment_details
from hackerstash.models.user import User
from hackerstash.models.member import Member
from hackerstash.models.project import Project
from hackerstash.models.invite import Invite
from hackerstash.utils.auth import login_required, member_required, published_project_required

projects = Blueprint('projects', __name__)


@projects.route('/projects')
def index() -> str:
    filtered_projects = project_filtering(request.args)
    filters_count = len([x for x in list(request.args.keys()) if x != 'sorting'])
    results, pagination = paginate(filtered_projects)

    return render_template(
        'projects/index.html',
        filtered_projects=results,
        filters_count=filters_count,
        pagination=pagination
    )


@projects.route('/projects/<project_id>')
def show(project_id: str) -> str:
    project = Project.query.get(project_id)

    if not project:
        return render_template('projects/404.html')
    # You shouldn't ever see the project page until
    # it's published
    if not project.published:
        return redirect(url_for('projects.edit', project_id=project.id))

    return render_template('projects/show.html', project=project)


@projects.route('/projects/create')
@login_required
def create() -> str:
    now = datetime.datetime.now()
    user = User.query.get(g.user.id)

    if user.member:
        return redirect(url_for('projects.show', project_id=user.member.project.id))

    project = Project(name='Untitled', time_commitment='FULL_TIME', start_month=now.month - 1, start_year=now.year)
    member = Member(owner=True, user=user, project=project)

    db.session.add(project)
    db.session.add(member)
    db.session.commit()

    return redirect(url_for('projects.edit', project_id=project.id))


@projects.route('/projects/<project_id>/edit')
@login_required
@member_required
def edit(project_id: str) -> str:
    project = Project.query.get(project_id)
    return render_template('projects/edit.html', project=project)


@projects.route('/projects/<project_id>/subscription')
@login_required
@member_required
def subscription(project_id: str) -> str:
    project = Project.query.get(project_id)
    # This is for the owner only!
    if not g.user.member.owner:
        return render_template('projects/401.html')
    if not project.published:
        return redirect(url_for('projects.show', project_id=project_id))
    payment_details = get_payment_details(g.user)
    return render_template('projects/subscription/index.html', project=project, payment_details=payment_details)


@projects.route('/projects/<project_id>/posts')
def all_posts(project_id: str) -> str:
    project = Project.query.get(project_id)
    return render_template('projects/posts/index.html', project=project)


@projects.route('/projects/<project_id>/update', methods=['POST'])
@login_required
@member_required
def update(project_id: str) -> str:
    project = Project.query.get(project_id)

    # Flask adds the empty file for some reason
    if 'file' in request.files and request.files['file'].filename != '':
        key = Images.upload(request.files['file'])
        project.avatar = key
    elif 'avatar' in request.form and not request.form['avatar'] and project.avatar:
        Images.delete(project.avatar)
        project.avatar = None

    for key, value in request.form.items():
        if key not in ['file', 'avatar']:
            # TODO Fix limiting
            value = value[:280] if key == 'description' else value
            # Rich text always uses body as the key
            key = 'description' if key == 'body' else key
            setattr(project, key, value)

    lists = ['fundings', 'business_models', 'platforms_and_devices']

    for key in lists:
        val = request.form.getlist(key)
        if val:
            setattr(project, key, val)

    db.session.commit()
    return redirect(url_for('projects.show', project_id=project.id, saved=1))


@projects.route('/projects/<project_id>/delete')
@login_required
@member_required
def destroy(project_id: str) -> str:
    project = Project.query.get(project_id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('projects.index'))


@projects.route('/projects/<project_id>/members/add')
@login_required
@member_required
def add_members(project_id: str) -> str:
    project = Project.query.get(project_id)
    return render_template('projects/members/add.html', project=project)


@projects.route('/projects/<project_id>/members/<member_id>/edit')
@login_required
@member_required
def edit_member(project_id: str, member_id: str) -> str:
    project = Project.query.get(project_id)
    match = [m for m in project.members if m.id == int(member_id)]
    return render_template('projects/members/edit.html', project=project, member=match[0])


@projects.route('/projects/<project_id>/members/<member_id>/edit', methods=['POST'])
@login_required
@member_required
def update_member(project_id: str, member_id: str) -> str:
    member = Member.query.get(member_id)
    member.role = request.form['role']
    db.session.commit()
    return redirect(url_for('projects.edit', project_id=project_id, tab='team', saved=1))


@projects.route('/projects/<project_id>/members/<member_id>/delete')
@login_required
@member_required
def delete_member(project_id: str, member_id: str) -> str:
    member = Member.query.get(member_id)

    if member.owner:
        logging.info(f'{g.user.username} tried to delete the owner ({member.user.username})')
        flash('The project owner can\'t be deleted', 'failure')
        return redirect(url_for('projects.edit_member', project_id=project_id, member_id=member_id))

    notification_factory('member_removed', {'member': member, 'remover': g.user}).publish()

    db.session.delete(member)
    db.session.commit()

    if g.user.id == member.user.id:
        return redirect(url_for('users.show', user_id=member.user.id))
    else:
        return redirect(url_for('projects.edit', project_id=project_id, tab='team'))


@projects.route('/projects/<project_id>/members/create', methods=['POST'])
@login_required
@member_required
def invite_member(project_id: str) -> str:
    email = request.form['email']
    link = Invites.generate(email)
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
            notification_factory('member_invited', {'invite': invite, 'user': user, 'inviter': g.user}).publish()
        else:
            email_factory('invite_to_project', email, {'invite': invite, 'inviter': g.user}).send()

    return redirect(url_for('projects.edit', project_id=project.id, tab='team'))


@projects.route('/projects/<project_id>/invites/<invite_id>/delete')
@login_required
@member_required
def remove_invite(project_id: str, invite_id: str) -> str:
    invite = Invite.query.get(invite_id)
    db.session.delete(invite)
    db.session.commit()
    return redirect(url_for('projects.edit', project_id=project_id, tab='team'))


@projects.route('/projects/<project_id>/vote')
@login_required
@published_project_required
def vote_project(project_id: str) -> str:
    project = Project.query.get(project_id)
    size = request.args.get('size', 'lg')
    direction = request.args.get('direction', 'up')

    if project.id != g.user.member.project.id:
        project.vote(g.user, direction)

    if request.headers.get('X-Requested-With') == 'fetch':
        partial = get_template_attribute('partials/vote.html', 'project_vote')
        return partial(size, project)
    else:
        return redirect(url_for('projects.show', project_id=project.id))


@projects.route('/projects/invites/<invite_token>')
def accept_invite(invite_token: str) -> str:
    data = Invites.decode(invite_token)
    user = User.query.filter_by(email=data['email']).first()
    invite = Invite.query.filter_by(email=data['email']).first()

    if not invite:
        # The invite has been removed
        return redirect(url_for('home.index'))

    if user:
        member = Member(
            owner=False,
            role=invite.role,
            user=user,
            project=invite.project
        )

        db.session.add(member)
        db.session.delete(invite)
        db.session.commit()

        notification_factory('member_verified', {'member': member}).publish()
        return redirect(url_for('projects.show', project_id=invite.project.id))
    else:
        # They need to create an account first
        return redirect(url_for('auth.signup'))
