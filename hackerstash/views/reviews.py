from flask import Blueprint, render_template
from hackerstash.models.review import Review

reviews = Blueprint('reviews', __name__)


@reviews.route('/reviews')
def index() -> str:
    """
    Render the reviews page
    :return: str
    """
    all_reviews = Review.query.all()
    return render_template('reviews/index.html', reviews=all_reviews)
