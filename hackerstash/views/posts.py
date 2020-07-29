from flask import Blueprint, render_template
from hackerstash.lib.decorators import login_required
from hackerstash.models.post import Post

posts = Blueprint('posts', __name__)


@posts.route('/posts')
def index():
    return render_template('posts/index.html')


@posts.route('/create')
@login_required
def create():
    return render_template('posts/create.html')


@posts.route('/posts/<post_id>')
def show(post_id):
    post = Post.query.get(post_id)
    return render_template('posts/show.html', post=post)
