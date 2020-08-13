import csv
from io import StringIO
from flask import Blueprint, render_template, request, redirect, url_for, g, session, Response
from hackerstash.db import db
from hackerstash.models.admin import Admin
from hackerstash.models.user import User
from hackerstash.models.waitlist import Waitlist
from hackerstash.utils.auth import admin_login_required

admin_dashboard = Blueprint('admin_dashboard', __name__)


@admin_dashboard.route('/admin/dashboard')
@admin_login_required
def index() -> str:
    tab = request.args.get('tab', 'overview')
    data = {'users': [], 'admins': [], 'waitlist': []}

    if tab == 'overview':
        data['users'] = User.query.all()
    if tab == 'admins':
        data['admins'] = Admin.query.all()
    if tab == 'waitlist':
        data['waitlist'] = Waitlist.query.all()

    return render_template('admin/dashboard/index.html', **data)


@admin_dashboard.route('/admin/users/create', methods=['POST'])
@admin_login_required
def create_admin_user() -> str:
    admin = Admin(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        email=request.form['email'],
        password=request.form['password'],
        root=False
    )
    db.session.add(admin)
    db.session.commit()
    return redirect(url_for('admin_dashboard.index', tab='admins'))


@admin_dashboard.route('/admin/users/<user_id>/delete')
@admin_login_required
def delete_admin_user(user_id: str) -> str:
    user = Admin.query.get(user_id) or User.query.get(user_id)
    if user and not user.root:
        db.session.delete(user)
        db.session.commit()

        if user.id == g.admin_user.id:
            session.pop('admin_id', None)
            return redirect(url_for('home.index'))

    return redirect(url_for('admin_dashboard.index', tab='admins'))


@admin_dashboard.route('/admin/waitlist/download')
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
