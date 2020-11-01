from flask import Blueprint, render_template, request
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
        'user_count': User.query.count(),
        'project_count': Project.query.count()
    }

    if tab == 'users':
        data['users'] = User.query.order_by(User.created_at.desc()).paginate(page, 25, False)
    if tab == 'projects':
        data['projects'] = Project.query.order_by(Project.created_at.desc()).paginate(page, 25, False)

    return render_template('admin/index.html', **data)
