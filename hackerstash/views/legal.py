from flask import Blueprint, render_template

legal = Blueprint('legal', __name__)


@legal.route('/terms')
def terms() -> str:
    return render_template('legal/terms/index.html')


@legal.route('/privacy')
def privacy() -> str:
    return render_template('legal/privacy/index.html')
