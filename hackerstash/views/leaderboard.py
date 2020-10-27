import arrow
from flask import Blueprint, render_template
from hackerstash.lib.pagination import paginate
from hackerstash.models.project import Project

leaderboard = Blueprint('leaderboard', __name__)


@leaderboard.route('/leaderboard')
def index() -> str:
    remaining_days = arrow.utcnow().ceil('month').humanize(only_distance=True)
    projects = Project.query.filter_by(published=True).all()
    projects = sorted(projects, key=lambda x: x.position)
    results, pagination = paginate(projects)
    data = {'remaining_days': remaining_days, 'projects': results, 'pagination': pagination}
    return render_template('leaderboard/index.html', **data)
