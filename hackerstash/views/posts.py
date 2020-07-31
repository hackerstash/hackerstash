from flask import Blueprint, render_template, g, request, redirect, url_for
from hackerstash.db import db
from hackerstash.lib.auth_helpers import login_required, author_required
from hackerstash.models.user import User
from hackerstash.models.post import Post
from hackerstash.models.project import Project
from hackerstash.models.comment import Comment

posts = Blueprint('posts', __name__)


@posts.route('/posts')
def index():
    tab = request.args.get('tab', 'new')
    # TODO order by tab
    all_posts = Post.query.all()
    return render_template('posts/index.html', all_posts=all_posts)


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


@posts.route('/posts/<post_id>/edit')
@login_required
@author_required
def edit(post_id):
    post = Post.query.get(post_id)
    return render_template('posts/edit.html', post=post)


@posts.route('/posts/<post_id>/update', methods=['POST'])
@login_required
@author_required
def update(post_id):
    post = Post.query.get(post_id)

    post.title = request.form['title']
    post.body = request.form['body']
    db.session.commit()

    return render_template('posts/show.html', post=post)


@posts.route('/posts/<post_id>/destroy')
@login_required
@author_required
def destroy(post_id):
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('posts.index'))


@posts.route('/posts/<post_id>/comment', methods=['POST'])
@login_required
def comment(post_id):
    user = User.query.get(g.user.id)
    post = Post.query.get(post_id)

    comment = Comment(
        body=request.form['body'],
        parent_comment_id=request.form['parent_comment_id'] or None,
        user=user,
        post_id=post.id
    )

    post.comments.append(comment)
    db.session.commit()

    return redirect(url_for('posts.show', post_id=post_id))
