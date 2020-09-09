from flask import Blueprint, render_template, g, request, redirect, url_for, get_template_attribute, flash, jsonify
from hackerstash.db import db
from hackerstash.lib.images import upload_image
from hackerstash.lib.challenges.factory import challenge_factory
from hackerstash.lib.logging import logging
from hackerstash.lib.mentions import proccess_mentions, publish_post_mentions, publish_comment_mentions
from hackerstash.lib.notifications.factory import notification_factory
from hackerstash.lib.pagination import paginate
from hackerstash.models.user import User
from hackerstash.models.post import Post
from hackerstash.models.project import Project
from hackerstash.models.comment import Comment
from hackerstash.utils.auth import login_required, author_required, published_project_required

posts = Blueprint('posts', __name__)


@posts.route('/posts')
def index() -> str:
    tab = request.args.get('tab', 'new')

    if tab == 'following' and g.user:
        following_ids = [x.id for x in g.user.following]
        all_posts = Post.query.filter(Post.user_id.in_(following_ids))
    else:
        all_posts = Post.query.all()

    all_posts = sorted(all_posts, key=lambda x: x.created_at if tab == 'new' else x.vote_score, reverse=True)
    results, pagination = paginate(all_posts)
    return render_template('posts/index.html', all_posts=results, pagination=pagination)


@posts.route('/posts/<post_id>')
def show(post_id: str) -> str:
    # If they request the url with the id we should
    # attempt to redirect to the fancy url. This is
    # mostly for legacy and can probably be removed
    # one day
    if post_id.isnumeric():
        post = Post.query.get(post_id)
        if not post:
            return render_template('posts/404.html')
        logging.info(f'Redirecting post \'{post.id}\' as it was accessed via it\'s id')
        return redirect(url_for('posts.show', post_id=post.url_slug))

    post = Post.query.filter_by(url_slug=post_id).first()
    if not post:
        return render_template('posts/404.html')
    return render_template('posts/show.html', post=post)


@posts.route('/posts/new')
@login_required
@published_project_required
def new() -> str:
    return render_template('posts/new.html')


@posts.route('/posts/create', methods=['POST'])
@login_required
@published_project_required
def create() -> str:
    user = User.query.get(g.user.id)
    project = Project.query.get(g.user.member.project_id)

    if 'title' not in request.form or 'body' not in request.form:
        logging.info('Not all fields were submitted during post create: %s', request.form)
        flash('All fields are required', 'failure')
        return render_template('posts/new.html')

    if not project.published:
        return redirect(url_for('posts.index'))

    title = request.form['title']
    url_slug = Post.generate_url_slug(title)
    body, mentioned_users = proccess_mentions(request.form['body'])

    post = Post(title=title, body=body, user=user, url_slug=url_slug, project=project)
    db.session.add(post)
    db.session.commit()

    publish_post_mentions(mentioned_users, post)
    challenge_factory('post_created', {'post': post})
    notification_factory('post_created', {'post': post}).publish()

    return redirect(url_for('posts.show', post_id=post.url_slug))


@posts.route('/posts/images', methods=['POST'])
@login_required
@published_project_required
def upload_images():
    images = []
    for file in request.files.getlist('file'):
        images.append(upload_image(file))
    return jsonify(images)


@posts.route('/posts/<post_id>/edit')
@login_required
@author_required
def edit(post_id: str) -> str:
    post = Post.query.get(post_id)
    return render_template('posts/edit.html', post=post)


@posts.route('/posts/<post_id>/update', methods=['POST'])
@login_required
@author_required
def update(post_id: str) -> str:
    post = Post.query.get(post_id)
    title = request.form['title']
    body, mentioned_users = proccess_mentions(request.form['body'])

    if post.title != request.form['title']:
        post.url_slug = Post.generate_url_slug(title)

    post.title = title
    post.body = body

    db.session.commit()

    publish_post_mentions(mentioned_users, post)
    return redirect(url_for('posts.show', post_id=post.url_slug, saved=1))


@posts.route('/posts/<post_id>/destroy')
@login_required
@author_required
def destroy(post_id: str) -> str:
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('posts.index'))


@posts.route('/posts/<post_id>/comment', methods=['POST'])
@login_required
def create_comment(post_id: str) -> str:
    user = User.query.get(g.user.id)
    post = Post.query.get(post_id)

    if not request.form['body'] or not user.member.project.published:
        return redirect(url_for('posts.show', post_id=post.url_slug))

    body, mentioned_users = proccess_mentions(request.form['body'])
    parent_comment_id = request.form.get('parent_comment_id')
    # Some weirdness going on with bad values trying to get added
    parent_comment_id = parent_comment_id if parent_comment_id.isnumberic() else None
    comment = Comment(body=body, parent_comment_id=parent_comment_id, user=user, post_id=post.id)

    post.comments.append(comment)
    db.session.commit()

    publish_comment_mentions(mentioned_users, comment)
    challenge_factory('comment_created', {'comment': comment})
    notification_factory('comment_created', {'comment': comment}).publish()

    if request.headers.get('X-Requested-With') == 'fetch':
        partial = get_template_attribute('partials/comments.html', 'comments')
        return partial(comment.post.comments, True)
    else:
        return redirect(url_for('posts.show', post_id=post.url_slug))


@posts.route('/posts/<post_id>/comment/<comment_id>/delete')
@login_required
def delete_comment(post_id: str, comment_id: str) -> str:
    comment = Comment.query.get(comment_id)

    if comment.user.id == g.user.id:
        db.session.delete(comment)
        # If there are comments nested under the deleted comment
        # then just remove the reference. We'll probably need to
        # do something smarter later!
        for c in comment.post.comments:
            if c.parent_comment_id == int(comment_id):
                c.parent_comment_id = None
        db.session.commit()

    if request.headers.get('X-Requested-With') == 'fetch':
        partial = get_template_attribute('partials/comments.html', 'comments')
        return partial(comment.post.comments, True)
    else:
        return redirect(url_for('posts.show', post_id=comment.post.url_slug))


@posts.route('/posts/<post_id>/vote')
@login_required
@published_project_required
def post_vote(post_id: str) -> str:
    post = Post.query.get(post_id)
    size = request.args.get('size', 'lg')
    direction = request.args.get('direction', 'up')

    if post.project.id != g.user.member.project.id:
        post.vote(g.user, direction)
        challenge_factory('post_voted', {'post': post})
        notification_factory('post_voted', {'post': post, 'direction': direction, 'voter': g.user}).publish()

    if request.headers.get('X-Requested-With') == 'fetch':
        partial = get_template_attribute('partials/vote.html', 'post_vote')
        return partial(size, post)
    else:
        return redirect(url_for('posts.show', post_id=post.url_slug))


@posts.route('/posts/<post_id>/comment/<comment_id>')
@login_required
@published_project_required
def comment_vote(post_id: str, comment_id: str) -> str:
    comment = Comment.query.get(comment_id)
    direction = request.args.get('direction', 'up')

    if comment.user.member.project.id != g.user.member.project.id:
        comment.vote(g.user, direction)
        challenge_factory('comment_voted', {'comment': comment})
        notification_factory('comment_voted', {'comment': comment, 'direction': direction, 'voter': g.user}).publish()

    if request.headers.get('X-Requested-With') == 'fetch':
        partial = get_template_attribute('partials/comments.html', 'comments')
        return partial(comment.post.comments, True)
    else:
        return redirect(url_for('posts.show', post_id=post_id))
