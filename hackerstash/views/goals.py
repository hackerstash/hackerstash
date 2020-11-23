from flask import Blueprint, render_template, request, redirect, url_for, g
from hackerstash.db import db
from hackerstash.lib.goals import Goals, GoalStates
from hackerstash.lib.logging import Logging
from hackerstash.lib.posts import Posts
from hackerstash.models.feedback import Feedback
from hackerstash.models.goal import Goal
from hackerstash.models.project import Project
from hackerstash.utils.auth import login_required, published_project_required
from hackerstash.utils.helpers import find_in_list

log = Logging(module='Views::Goals')
goals = Blueprint('goals', __name__)


@goals.route('/goals', methods=['GET', 'POST'])
@login_required
@published_project_required
def index() -> str:
    project = g.user.project
    status = Goals(project).status()

    if status == GoalStates.NONE:
        return redirect(url_for('projects.show', project_id=project.id))
    if status == GoalStates.REFLECT:
        return redirect(url_for('goals.reflect'))
    if status == GoalStates.REVIEW:
        return redirect(url_for('goals.review'))
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
        # Tag#2 is for 'Ask HackerStash'
        Posts(title=request.form['title'], body=request.form['body'], tag_id='2').create()

    db.session.commit()
    return redirect(url_for('goals.index', submitted=1))


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


@goals.route('/goals/reflect', methods=['GET', 'POST'])
@login_required
def reflect() -> str:
    project = g.user.project
    complete = not request.args.get('edit') and any([goal.completed for goal in project.active_goals])

    if request.method == 'GET':
        return render_template('goals/reflect/index.html', project=project, complete=complete)

    log.info('Reflecting on goals', {'project_id': project.id, 'payload': request.form})

    for goal in project.active_goals:
        goal.completed = str(goal.id) in request.form.getlist('goals')
        goal.evidence = request.form.get(f'evidence_{goal.id}')

    db.session.commit()

    return redirect(url_for('goals.reflect'))


@goals.route('/goals/review', methods=['GET', 'POST'])
@login_required
def review() -> str:
    project = g.user.project

    if request.method == 'GET':
        return render_template('goals/review/index.html', project=project)

    log.info('Reviewing goals', {'project_id': project.id, 'payload': request.form})

    for feedback in project.reviews_to_give:
        feedback.feedback = request.form.get(f'project-{feedback.id}-feedback')
        feedback.position = int(request.form.get(f'project-{feedback.id}-position'))
        db.session.commit()

    return redirect(url_for(request.endpoint))