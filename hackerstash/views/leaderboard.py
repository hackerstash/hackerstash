from sqlalchemy import func
from flask import Blueprint, render_template, request
from hackerstash.lib.leaderboard import Leaderboard
from hackerstash.models.project import Project

leaderboard = Blueprint('leaderboard', __name__)


@leaderboard.route('/leaderboard')
def index() -> str:
    page = request.args.get('page', 1, type=int)

    order = Leaderboard.order()
    remaining_days = Leaderboard.remaining_days()
    order_expr = func.array_position(order, Project.id)

    projects = Project.query\
        .filter(Project.id.in_(order))\
        .filter(Project.published == True)\
        .order_by(order_expr)\
        .paginate(page, 25, False)

    return render_template('leaderboard/index.html', remaining_days=remaining_days, paginated_projects=projects)
