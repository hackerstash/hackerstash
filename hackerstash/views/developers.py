from flask import Blueprint, render_template

developers = Blueprint('developers', __name__)


@developers.route('/developers')
def index() -> str:
    return render_template('developers/index.html')
