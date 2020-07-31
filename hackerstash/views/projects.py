from flask import Blueprint, render_template, redirect, url_for, g, request
from hackerstash.db import db
from hackerstash.lib.auth_helpers import login_required, member_required
from hackerstash.lib.images import upload_image, delete_image
from hackerstash.models.user import User
from hackerstash.models.member import Member
from hackerstash.models.project import Project

projects = Blueprint('projects', __name__)


@projects.route('/projects')
def index():
    all_projects = Project.query.filter_by(published=True)
    return render_template('projects/index.html', projects=all_projects)


@projects.route('/projects/<project_id>')
def show(project_id):
    project = Project.query.get(project_id)
    return render_template('projects/show.html', project=project)


@projects.route('/projects/create')
@login_required
def create():
    user = User.query.get(g.user.id)

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
    elif not request.form['avatar'] and project.avatar:
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
