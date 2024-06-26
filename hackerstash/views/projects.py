from flask import Blueprint, render_template, redirect, url_for, g, request, flash, get_template_attribute
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.attributes import flag_modified
from hackerstash.db import db
from hackerstash.lib.feed import Feed
from hackerstash.lib.images import Images
from hackerstash.lib.invites import Invites
from hackerstash.lib.emails.factory import email_factory
from hackerstash.lib.leaderboard import Leaderboard
from hackerstash.lib.logging import Logging
from hackerstash.lib.notifications.factory import notification_factory
from hackerstash.lib.challenges.factory import challenge_factory
from hackerstash.models.user import User
from hackerstash.models.member import Member
from hackerstash.models.project import Project
from hackerstash.models.invite import Invite
from hackerstash.utils.auth import login_required, member_required, published_project_required
from hackerstash.utils.helpers import get_html_text_length

log = Logging(module='Views::Project')
projects = Blueprint('projects', __name__)


@projects.route('/projects')
def index() -> str:
    """
    Render the project list page
    :return: str
    """
    order_by = None
    sort = request.args.get('sorting', 'project_score_desc')
    page = request.args.get('page', 1, type=int)

    if sort == 'alphabetical_asc':
        order_by = Project.name.asc()
    if sort == 'alphabetical_desc':
        order_by = Project.name.desc()
    if sort == 'created_at_desc':
        order_by = Project.created_at.desc()
    if sort == 'updated_at_asc':
        order_by = Project.updated_at.asc()
    if sort == 'team_size_asc':
        order_by = Project.team_size.asc()
    if sort == 'team_size_desc':
        order_by = Project.team_size.desc()
    if sort == 'project_score_asc':
        order_by = func.array_position(Leaderboard.order(reverse=True), Project.id)
    if sort == 'project_score_desc':
        order_by = func.array_position(Leaderboard.order(), Project.id)

    paginated_projects = Project.query\
        .filter(Project.published==True)\
        .options(joinedload(Project.members))\
        .order_by(order_by)\
        .paginate(page, 24, False)
    return render_template('projects/index.html', paginated_projects=paginated_projects)


@projects.route('/projects/<project_id>')
def show(project_id: str) -> str:
    """
    Render the project show page
    :param project_id: str
    :return: str
    """
    project = Project.query.get(project_id)

    if not project:
        return render_template('projects/404.html')
    # You shouldn't ever see the project page until
    # it's published
    if not project.published:
        return redirect(url_for('projects.edit', project_id=project.id))

    return render_template('projects/show.html', project=project, feed=Feed(project))


@projects.route('/projects/<project_id>/feed')
def feed(project_id: str) -> str:
    """
    Render the feed partial for the project page
    :param project_id: str
    :return: str
    """
    project = Project.query.get(project_id)
    if request.headers.get('X-Requested-With') == 'fetch':
        return render_template('partials/feed.html', project=project, feed=Feed(project))
    else:
        return redirect(url_for('projects.show', **request.args, **request.view_args))


@projects.route('/projects/<project_id>/posts')
def all_posts(project_id: str) -> str:
    """
    Render all the posts for a project
    :param project_id: str
    :return: str
    """
    project = Project.query.get(project_id)
    return render_template('projects/posts.html', project=project)


@projects.route('/projects/<project_id>/edit', methods=['GET', 'POST'])
@login_required
@member_required
def edit(project_id: str) -> str:
    """
    Render or update the project edit page
    :param project_id: str
    :return: str
    """
    project = Project.query.get(project_id)

    if request.method == 'GET':
        return render_template('projects/edit.html', project=project)

    log.info('Updating project', {'project_id': project.id, 'user_id': g.user.id, 'project_data': request.form})

    if get_html_text_length(request.form.get('body')) > 240:
        flash('Project description exceeds 240 characters', 'failure')
        return redirect(url_for('projects.edit', project_id=project.id))

    # Flask adds the empty file for some reason
    if 'file' in request.files and request.files['file'].filename != '':
        key = Images.upload(request.files['file'])
        project.avatar = key
    elif 'avatar' in request.form and not request.form['avatar'] and project.avatar:
        Images.delete(project.avatar)
        project.avatar = None

    for key, value in request.form.items():
        if key not in ['file', 'avatar', 'profile_button_text', 'profile_button_url']:
            # Rich text always uses body as the key
            key = 'description' if key == 'body' else key
            # This needs to be a boolean, not a string
            value = value == 'true' if key == 'looking_for_cofounders' else value
            setattr(project, key, value)

    lists = ['fundings', 'business_models', 'platforms_and_devices']

    for key in lists:
        val = request.form.getlist(key)
        if val:
            setattr(project, key, val)

    # Update the profile button seperately
    if request.form.get('profile_button_text'):
        project.profile_button = {
            'url': request.form.get('profile_button_url'),
            'text': request.form.get('profile_button_text')
        }
        flag_modified(project, 'profile_button')

    db.session.commit()
    return redirect(url_for('projects.show', project_id=project.id, saved=1))


@projects.route('/projects/<project_id>/upload_header', methods=['POST'])
@login_required
@member_required
def upload_header(project_id: str) -> str:
    """
    Update the project header banner
    :param project_id: str
    :return: str
    """
    project = Project.query.get(project_id)
    log.info('Updating project header', {'project_id': project.id, 'user_id': g.user.id})

    if 'header_file' in request.files and request.files['header_file'].filename != '':
        key = Images.upload(request.files['header_file'])
        project.banner = key
        db.session.commit()
    return redirect(url_for('projects.edit', project_id=project.id))


@projects.route('/projects/<project_id>/delete_header')
@login_required
@member_required
def delete_header(project_id: str) -> str:
    """
    Remove a member from the project
    :param project_id: str
    :return: str
    """
    project = Project.query.get(project_id)
    log.info('Deleting project header', {'project_id': project.id, 'user_id': g.user.id})

    if project.banner:
        Images.delete(project.banner)
        project.banner = None
        db.session.commit()
    return redirect(url_for('projects.edit', project_id=project.id))


@projects.route('/projects/publish')
@login_required
@member_required
def publish() -> str:
    """
    Publish a project
    :return: str
    """
    project = g.user.project
    project.published = True
    db.session.commit()
    return redirect(url_for('projects.show', project_id=project.id))


@projects.route('/projects/unpublish')
@login_required
@member_required
def unpublish() -> str:
    """
    Unpublish a project
    :return: str
    """
    project = g.user.project
    project.published = False
    db.session.commit()
    return redirect(url_for('projects.show', project_id=project.id))


@projects.route('/projects/delete')
@login_required
@member_required
def destroy() -> str:
    """
    Delete a project
    :return:
    """
    project = g.user.project
    log.info('Deleting project', {'project_id': project.id, 'user_id': g.user.id})
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('projects.index'))


@projects.route('/projects/<project_id>/members/add')
@login_required
@member_required
def add_members(project_id: str) -> str:
    """
    Render the new member page
    :param project_id: str
    :return: str
    """
    project = Project.query.get(project_id)
    return render_template('projects/members/add.html', project=project)


@projects.route('/projects/<project_id>/members/<member_id>/edit')
@login_required
@member_required
def edit_member(project_id: str, member_id: str) -> str:
    """
    Render the member edit page
    :param project_id: str
    :param member_id: str
    :return: str
    """
    project = Project.query.get(project_id)
    match = [m for m in project.members if m.id == int(member_id)]
    return render_template('projects/members/edit.html', project=project, member=match[0])


@projects.route('/projects/<project_id>/members/<member_id>/edit', methods=['POST'])
@login_required
@member_required
def update_member(project_id: str, member_id: str) -> str:
    """
    Update a member
    :param project_id: str
    :param member_id: str
    :return: str
    """
    member = Member.query.get(member_id)
    log.info('Updating team member', {'member_id': member.id, 'member_data': request.form})
    member.role = request.form['role']
    db.session.commit()
    return redirect(url_for('projects.edit', project_id=project_id, tab='team', saved=1))


@projects.route('/projects/<project_id>/members/<member_id>/delete')
@login_required
@member_required
def delete_member(project_id: str, member_id: str) -> str:
    """
    Delete a member
    :param project_id: str
    :param member_id: str
    :return:
    """
    member = Member.query.get(member_id)
    log.info('Deleting team member', {'member_id': member.id, 'user_id': g.user.id})

    if member.owner:
        log.warn('Someone tried to delete the owner', {'user_id': g.user.id, 'owner_user_id': member.user.id})
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
    """
    Invite a new member
    :param project_id: str
    :return: str
    """
    email = request.form['email']
    link = Invites.generate(email)
    user = User.query.filter_by(email=email).first()
    project = Project.query.get(project_id)
    is_already_member = user and user.project

    log.info('Inviting team member', {'email': email, 'is_already_member': is_already_member})

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
    """
    Cancel an invite
    :param project_id: str
    :param invite_id: str
    :return: str
    """
    log.info('Removing invite', {'project_id': project_id, 'invite_id': invite_id})
    invite = Invite.query.get(invite_id)
    db.session.delete(invite)
    db.session.commit()
    return redirect(url_for('projects.edit', project_id=project_id, tab='team'))


@projects.route('/projects/<project_id>/vote')
@login_required
@published_project_required
def vote_project(project_id: str) -> str:
    """
    Vote for a project
    :param project_id: str
    :return: str
    """
    project = Project.query.get(project_id)
    size = request.args.get('size', 'lg')
    direction = request.args.get('direction', 'up')

    log.info('Voting project', {'user_id': g.user.id, 'project_id': project.id, 'direction': direction})

    if project.id != g.user.project.id:
        project.vote(g.user, direction)
        challenge_factory('project_voted', {})

    if request.headers.get('X-Requested-With') == 'fetch':
        partial = get_template_attribute('partials/vote.html', 'project_vote')
        return partial(size, project)
    else:
        return redirect(url_for('projects.show', project_id=project.id))


@projects.route('/projects/invites/<invite_token>')
def accept_invite(invite_token: str) -> str:
    """
    Accept an invite to a project
    :param invite_token: str
    :return: str
    """
    data = Invites.decode(invite_token)
    user = User.query.filter_by(email=data['email']).first()
    invite = Invite.query.filter_by(email=data['email']).first()

    log.info('Accepting invite', {'data': data})

    if not invite:
        log.warn('Invite does not exist', {'data': data})
        # The invite has been removed
        return redirect(url_for('home.index'))

    if user:
        log.info('Creating member', {'user_id': user.id, 'data': data})
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
