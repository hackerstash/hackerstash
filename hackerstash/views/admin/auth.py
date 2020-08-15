from flask import Blueprint, render_template, request, redirect, flash, url_for, session
from hackerstash.models.admin import Admin

admin_auth = Blueprint('admin_auth', __name__)


@admin_auth.route('/admin', methods=['GET', 'POST'])
def index() -> str:
    if request.method == 'GET':
        return render_template('admin/auth/index.html')

    admin = Admin.query.filter_by(email=request.form['email']).first()
    valid = admin.validate_password(request.form['password']) if admin else False

    if valid:
        session['admin_id'] = admin.id
        return redirect(url_for('admin_dashboard.index'))
    else:
        flash('Nope!', 'failure')
        return redirect(url_for('admin_auth.index'))


@admin_auth.route('/admin/signout')
def signout() -> str:
    session.pop('admin_id', None)
    return redirect(url_for('home.index'))
