import json
from flask import Blueprint, render_template, g, request, redirect, url_for, get_template_attribute, flash
from hackerstash.db import db
from hackerstash.lib.images import upload_image
from hackerstash.lib.notifications.factory import notification_factory
from hackerstash.models.user import User
from hackerstash.models.post import Post
from hackerstash.models.project import Project
from hackerstash.models.comment import Comment
from hackerstash.models.image import Image
from hackerstash.utils.auth import login_required, author_required, published_project_required

posts = Blueprint('posts', __name__)


@posts.route('/posts')
def index():
    tab = request.args.get('tab', 'new')
    all_posts = Post.query.all()
    all_posts = sorted(all_posts, key=lambda x: x.created_at if tab == 'new' else x.vote_score, reverse=True)

    return render_template('posts/index.html', all_posts=all_posts)


@posts.route('/posts/<post_id>')
def show(post_id):
    post = Post.query.get(post_id)

    if not post:
        return render_template('posts/404.html')

    return render_template('posts/show.html', post=post)


@posts.route('/posts/new')
@login_required
@published_project_required
def new():
    return render_template('posts/new.html')


@posts.route('/posts/create', methods=['POST'])
@login_required
@published_project_required
def create():
    user = User.query.get(g.user.id)
    project = Project.query.get(g.user.member.project_id)

    if 'title' not in request.form or 'body' not in request.form:
        flash('All fields are required')
        return render_template('posts/new.html')

    post = Post(title=request.form['title'], body=request.form['body'], user=user, project=project)

    # filenames_to_upload will contain a list of images
    # that the user has not deleted. FileList is readonly
    # on the front end.
    file_names = json.loads(request.form.get('filenames_to_upload', '[]'))

    for file in request.files.getlist('file'):
        if file.filename in file_names:
            key = upload_image(file)
            image = Image(key=key, file_name=file.filename)
            post.images.append(image)

    db.session.add(post)
    db.session.commit()

    notification_factory('post_created', {'post': post}).publish()

    return redirect(url_for('posts.show', post_id=post.id))


@posts.route('/posts/<post_id>/edit')
@login_required
@author_required
def edit(post_id):
    post = Post.query.get(post_id)
    image_list = json.dumps([image.file_name for image in post.images])
    return render_template('posts/edit.html', post=post, image_list=image_list)


@posts.route('/posts/<post_id>/update', methods=['POST'])
@login_required
@author_required
def update(post_id):
    post = Post.query.get(post_id)

    # TODO work out old/new images

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
        parent_comment_id=request.form.get('parent_comment_id'),
        user=user,
        post_id=post.id
    )

    post.comments.append(comment)
    db.session.commit()

    notification_factory('comment_created', {'comment': comment}).publish()

    if request.headers.get('X-Requested-With') == 'fetch':
        partial = get_template_attribute('partials/comments.html', 'comments')
        return partial(comment.post.comments, True)
    else:
        return redirect(url_for('posts.show', post_id=post_id))


@posts.route('/posts/<post_id>/vote')
@login_required
@published_project_required
def post_vote(post_id):
    post = Post.query.get(post_id)
    size = request.args.get('size', 'lg')
    direction = request.args.get('direction', 'up')

    if post.project.id != g.user.member.project.id:
        post.vote(g.user, direction)
        notification_factory('post_voted', {'post': post, 'direction': direction, 'voter': g.user}).publish()

    if request.headers.get('X-Requested-With') == 'fetch':
        partial = get_template_attribute('partials/vote.html', 'post_vote')
        return partial(size, post)
    else:
        return redirect(url_for('posts.show', post_id=post.id))


@posts.route('/posts/<post_id>/comment/<comment_id>')
@login_required
@published_project_required
def comment_vote(post_id, comment_id):
    comment = Comment.query.get(comment_id)
    direction = request.args.get('direction', 'up')

    if comment.user.member.project.id != g.user.member.project.id:
        comment.vote(g.user, direction)
        notification_factory('comment_voted', {'comment': comment, 'direction': direction, 'voter': g.user}).publish()

    if request.headers.get('X-Requested-With') == 'fetch':
        partial = get_template_attribute('partials/comments.html', 'comments')
        return partial(comment.post.comments, True)
    else:
        return redirect(url_for('posts.show', post_id=post_id))
