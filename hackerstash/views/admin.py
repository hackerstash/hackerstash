from flask import Blueprint, render_template, request, redirect, url_for
from hackerstash.db import db
from hackerstash.lib.sidebar import Sidebar
from hackerstash.models.contest import Contest
from hackerstash.models.project import Project
from hackerstash.models.user import User
from hackerstash.utils.auth import admin_login_required

admin = Blueprint('admin', __name__)


@admin.route('/admin')
@admin_login_required
def index() -> str:
    tab = request.args.get('tab', 'users')
    page = request.args.get('page', 1, type=int)
    data = {
        'users': {},
        'projects': {},
        'contests': [],
        'user_count': User.query.count(),
        'project_count': Project.query.count()
    }

    if tab == 'users':
        data['users'] = User.query.order_by(User.created_at.desc()).paginate(page, 25, False)
    if tab == 'projects':
        data['projects'] = Project.query.order_by(Project.created_at.desc()).paginate(page, 25, False)
    if tab == 'tournaments':
        data['contests'] = Contest.query.order_by(Contest.created_at.desc()).all()

    return render_template('admin/index.html', **data)


@admin.route('/admin/tournament')
@admin_login_required
def tournament() -> str:
    contest_id = request.args.get('id')
    contest = Contest.query.get(contest_id) if contest_id else Contest.get_current()
    data = {
        'contest': contest,
        'project_count': Project.query.filter_by(published=True).count()
    }
    return render_template('admin/tournament/index.html', **data)


@admin.route('/admin/tournament/<contest_id>/update', methods=['POST'])
@admin_login_required
def update_tournament(contest_id: str) -> str:
    contest = Contest.query.get(contest_id)
    contest.top_up = request.form['top_up']
    contest.prizes = {}
    for i in range(200):
        contest.prizes[f'prize_{i}'] = int(request.form.get(f'prize_{i}', 0))
    db.session.commit()
    Sidebar.clear_cache()
    return redirect(url_for('admin.index', tab='tournaments'))
