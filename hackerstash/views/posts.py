from flask import Blueprint, render_template, g, request, redirect, url_for
from hackerstash.db import db
from hackerstash.lib.decorators import login_required
from hackerstash.models.user import User
from hackerstash.models.post import Post
from hackerstash.models.project import Project

posts = Blueprint('posts', __name__)


@posts.route('/posts')
def index():
    posts = Post.query.all()
    return render_template('posts/index.html', all_posts=posts)


@posts.route('/posts/<post_id>')
def show(post_id):
    post = Post.query.get(post_id)
    return render_template('posts/show.html', post=post)


@posts.route('/posts/new')
@login_required
def new():
    return render_template('posts/new.html')


@posts.route('/posts/create', methods=['POST'])
@login_required
def create():
    # TODO auth
    user = User.query.get(g.user.id)
    project = Project.query.get(g.user.member.project_id)

    post = Post(title=request.form['title'], body=request.form['body'], user=user, project=project)
    db.session.add(post)
    db.session.commit()

    return redirect(url_for('posts.show', post_id=post.id))
