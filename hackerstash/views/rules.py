from flask import Blueprint, render_template

rules = Blueprint('rules', __name__)


@rules.route('/rules')
def index() -> str:
    return render_template('rules/index.html')
