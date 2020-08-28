from flask import Blueprint, render_template
from sqlalchemy.orm import joinedload
from hackerstash.models.project import Project

leaderboard = Blueprint('leaderboard', __name__)


@leaderboard.route('/leaderboard')
def index() -> str:
    projects = Project.query.filter_by(published=True).all()
    projects = sorted(projects, key=lambda x: x.vote_score, reverse=True)
    return render_template('leaderboard/index.html', projects=projects)
