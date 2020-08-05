from flask import Blueprint, render_template

legal = Blueprint('legal', __name__)


@legal.route('/terms')
def terms():
    return render_template('legal/terms/index.html')


@legal.route('/privacy')
def privacy():
    return render_template('legal/privacy/index.html')
