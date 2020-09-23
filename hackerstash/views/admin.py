import csv
from io import StringIO
from flask import Blueprint, render_template, request, redirect, url_for, Response
from hackerstash.db import db
from hackerstash.models.contest import Contest
from hackerstash.models.project import Project
from hackerstash.models.user import User
from hackerstash.models.waitlist import Waitlist
from hackerstash.utils.auth import admin_login_required

admin = Blueprint('admin', __name__)


@admin.route('/admin')
@admin_login_required
def index() -> str:
    tab = request.args.get('tab', 'overview')
    data = {'users': [], 'admins': [], 'waitlist': []}

    if tab == 'overview':
        data['users'] = User.query.all()
    if tab == 'projects':
        data['projects'] = Project.query.all()
    if tab == 'waitlist':
        data['waitlist'] = Waitlist.query.all()
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
    return redirect(url_for('admin.index', tab='tournaments'))


@admin.route('/admin/waitlist/download')
@admin_login_required
def download_waitlist():
    waitlist = Waitlist.query.all()

    string = StringIO()
    writer = csv.writer(string)
    writer.writerow(['first_name', 'email', 'created_at'])

    for w in waitlist:
        writer.writerow([w.first_name, w.email, w.created_at])

    return Response(
        string.getvalue(),
        mimetype='text/csv',
        headers={
            'Content-disposition': 'attachment; filename=waitlist.csv'
        }
    )
