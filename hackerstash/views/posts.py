from flask import Blueprint, render_template

posts = Blueprint('posts', __name__)


@posts.route('/posts')
def index():
    return render_template('posts/index.html')
