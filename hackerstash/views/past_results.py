from flask import Blueprint, render_template
from hackerstash.models.contest import Contest

past_results = Blueprint('past_results', __name__)


@past_results.route('/past_results')
def index() -> str:
    contests = Contest.query.all()
    return render_template('past_results/index.html', contests=contests)


@past_results.route('/past_results/<contest_id>')
def show(contest_id: str) -> str:
    contest = Contest.query.get(contest_id)
    return render_template('past_results/show.html', contest=contest)
