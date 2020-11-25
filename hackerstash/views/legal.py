from flask import Blueprint, render_template

legal = Blueprint('legal', __name__)


@legal.route('/terms')
def terms() -> str:
    """
    Render the terms page
    :return: str
    """
    return render_template('legal/terms.html')


@legal.route('/privacy')
def privacy() -> str:
    """
    Render the privacy page
    :return: str
    """
    return render_template('legal/privacy.html')
