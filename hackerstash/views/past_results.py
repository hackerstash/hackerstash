from flask import Blueprint, render_template

past_results = Blueprint('past_results', __name__)


@past_results.route('/past_results')
def index():
    return render_template('past_results/index.html')
