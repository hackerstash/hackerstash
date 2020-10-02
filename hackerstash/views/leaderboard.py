from flask import Blueprint, render_template
from hackerstash.lib.pagination import paginate
from hackerstash.models.project import Project

leaderboard = Blueprint('leaderboard', __name__)


@leaderboard.route('/leaderboard')
def index() -> str:
    projects = Project.query.filter_by(published=True).all()
    projects = sorted(projects, key=lambda x: x.vote_score, reverse=True)
    results, pagination = paginate(projects)
    return render_template('leaderboard/index.html', projects=results, pagination=pagination)
