from flask import Blueprint, render_template, request, redirect, url_for, g, session
from hackerstash.db import db
from hackerstash.models.admin import Admin
from hackerstash.utils.auth import admin_login_required

admin_dashboard = Blueprint('admin_dashboard', __name__)


@admin_dashboard.route('/admin/dashboard')
@admin_login_required
def index():
    tab = request.args.get('tab', 'overview')
    admins = []

    if tab == 'admins':
        admins = Admin.query.all()

    return render_template('admin/dashboard/index.html', admins=admins)


@admin_dashboard.route('/admin/users/create', methods=['POST'])
@admin_login_required
def create_admin_user():
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
def delete_admin_user(user_id):
    admin = Admin.query.get(user_id)
    if admin and not admin.root:
        db.session.delete(admin)
        db.session.commit()

        if admin.id == g.admin_user.id:
            session.pop('admin_id', None)
            return redirect(url_for('home.index'))

    return redirect(url_for('admin_dashboard.index', tab='admins'))
