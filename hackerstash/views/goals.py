from flask import Blueprint, render_template, request, redirect, url_for, g
from hackerstash.db import db
from hackerstash.lib.logging import Logging
from hackerstash.models.goal import Goal
from hackerstash.models.post import Post
from hackerstash.utils.auth import login_required, published_project_required
from hackerstash.utils.helpers import find_in_list

log = Logging(module='Views::Goals')
goals = Blueprint('goals', __name__)


@goals.route('/goals', methods=['GET', 'POST'])
@login_required
@published_project_required
def index() -> str:
    project = g.user.project

    if request.method == 'GET':
        return render_template('goals/index.html', project=project)

    log.info('Creating goals', {'project_id': project.id, 'payload': request.form})

    # Create all the goals
    for goal in ['goal_1', 'goal_2', 'goal_3']:
        value = request.form.get(goal)
        goal = Goal(name=value, project=project)
        db.session.add(goal)

    # Create a post if they added that information
    if request.form['title'] and request.form['body']:
        # TODO
        pass

    db.session.commit()
    return redirect(url_for('goals.index'))


@goals.route('/goals/edit', methods=['GET', 'POST'])
@login_required
@published_project_required
def edit() -> str:
    project = g.user.project

    if request.method == 'GET':
        return render_template('goals/edit.html', project=project)

    log.info('Updating goals', {'project_id': project.id, 'payload': request.form})

    for goal_id, name in request.form.items():
        goal = find_in_list(project.active_goals, lambda x: x.id == int(goal_id))
        goal.name = name

    db.session.commit()

    return redirect(url_for('goals.index'))
