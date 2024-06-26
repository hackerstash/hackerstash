from flask import Blueprint, render_template, g, request, redirect, url_for, get_template_attribute, flash, jsonify
from hackerstash.db import db
from hackerstash.lib.images import Images
from hackerstash.lib.challenges.factory import challenge_factory
from hackerstash.lib.logging import Logging
from hackerstash.lib.emails.factory import email_factory
from hackerstash.lib.mentions import Mentions
from hackerstash.lib.notifications.factory import notification_factory
from hackerstash.lib.posts import Posts
from hackerstash.models.post import Post
from hackerstash.models.comment import Comment
from hackerstash.models.tag import Tag
from hackerstash.utils.auth import login_required, author_required, published_project_required

log = Logging(module='Views::Posts')
posts = Blueprint('posts', __name__)


@posts.route('/posts')
def index() -> str:
    """
    Render the page list view
    :return: str
    """
    tab = request.args.get('tab', 'new')
    data = {'groups_list': None, 'paginated_posts': []}

    if tab == 'following' and 'user' in g:
        data['paginated_posts'] = Post.following()
    if tab == 'new':
        data['paginated_posts'] = Post.newest()
    if tab == 'top':
        data['paginated_posts'] = Post.top()
    if tab == 'groups':
        data['groups_list'] = Post.groups()

    return render_template('posts/index.html', **data)


@posts.route('/posts/tags/<tag_id>')
def tags(tag_id: str) -> str:
    """
    Render the page view showing individual tags
    :param tag_id: str
    :return: str
    """
    tag = Tag.query.get(tag_id)
    if not tag:
        return redirect(url_for('posts.index'))
    page = request.args.get('page', 1, type=int)
    paginated_posts = Post.query.filter_by(tag_id=tag.id).paginate(page, 25, False)
    return render_template('posts/tags.html', paginated_posts=paginated_posts, tag=tag)


@posts.route('/posts/tags/<tag_id>/follow')
@login_required
def follow_tag(tag_id: str) -> str:
    """
    Follow a particular tag
    :param tag_id: str
    :return: str
    """
    user = g.user
    tag = Tag.query.get(tag_id)
    if tag.has_user(user):
        log.info('Leaving group', {'user_id': user.id, 'tag_id': tag.id})
        tag.unfollow(user)
    else:
        log.info('Joining group', {'user_id': user.id, 'tag_id': tag.id})
        tag.follow(user)
    db.session.commit()
    return redirect(url_for('posts.tags', tag_id=tag.id))


@posts.route('/posts/<post_id>')
def show(post_id: str) -> str:
    """
    Show a post
    :param post_id: str
    :return: str
    """
    # If they request the url with the id we should
    # attempt to redirect to the fancy url. This is
    # mostly for legacy and can probably be removed
    # one day
    if post_id.isnumeric():
        post = Post.query.get(post_id)
        if not post:
            return render_template('posts/404.html')
        log.info('Redirecting post as it was accessed by the id', {'post_id': post.id})
        return redirect(url_for('posts.show', post_id=post.url_slug))

    post = Post.query.filter_by(url_slug=post_id).first()
    if not post:
        return render_template('posts/404.html')
    return render_template('posts/show.html', post=post)


@posts.route('/posts/new', methods=['GET', 'POST'])
@login_required
@published_project_required
def new() -> str:
    """
    Render or create a new post
    :return: str
    """
    if request.method == 'GET':
        return render_template('posts/new.html', tags=Tag.query.all())

    log.info('Creating new post', {'user_id': g.user.id, 'project_id': g.user.project.id, 'post_data': request.form})

    if 'title' not in request.form or 'body' not in request.form:
        log.warn('Not all fields were submitted during post create', {'request_data': request.form})
        flash('All fields are required', 'failure')
        return render_template('posts/new.html')

    p = Posts(title=request.form['title'], body=request.form['body'], tag_id=request.form.get('tag'))

    if request.form.get('post_type') == 'poll':
        question = request.form['question']
        choices = [x[1] for x in request.form.items() if x[0].startswith('choice_')]
        p.add_poll(question, choices)

    p.create()

    return redirect(url_for('posts.show', post_id=p.url_slug))


@posts.route('/posts/images', methods=['POST'])
@login_required
@published_project_required
def upload_images():
    """
    Upload some images
    :return: str
    """
    images = []
    for file in request.files.getlist('file'):
        images.append(Images.upload(file))
    return jsonify(images)


@posts.route('/posts/groups/request', methods=['POST'])
@login_required
@published_project_required
def request_group():
    """
    Request that we create a new group
    :return: str
    """
    tab = request.args.get('tab')
    payload = {
        'name': f'{g.user.first_name} {g.user.last_name}',
        'email': g.user.email,
        'subject': f'Group Request - {request.form["group_name"]}',
        'message': request.form['group_reason']
    }
    email_factory('contact', 'hello@hackerstash.com', payload).send()
    flash('Thanks, your group suggestion has been submitted')
    return redirect(url_for('posts.new', tab=tab))


@posts.route('/posts/<post_id>/update', methods=['GET', 'POST'])
@login_required
@author_required
def edit(post_id: str) -> str:
    """
    Render or update a post
    :param post_id: str
    :return: str
    """
    post = Post.query.get(post_id)

    if request.method == 'GET':
        return render_template('posts/edit.html', post=post, tags=Tag.query.all())

    title = request.form['title']
    tag_id = request.form.get('tag')
    mentions = Mentions(request.form['body'])

    log.info('Updating post', {'user_id': g.user.id, 'post_id': post.id, 'post_data': request.form})

    if post.title != request.form['title']:
        post.url_slug = Post.generate_url_slug(title)

    post.title = title
    post.body = mentions.body
    post.tag = Tag.query.get(tag_id) if tag_id else None

    db.session.commit()

    mentions.publish_post(post)
    return redirect(url_for('posts.show', post_id=post.url_slug, saved=1))


@posts.route('/posts/<post_id>/destroy')
@login_required
@author_required
def destroy(post_id: str) -> str:
    """
    Delete a post
    :param post_id: str
    :return: str
    """
    log.info('Deleting post', {'post_id': post_id})
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('posts.index'))


@posts.route('/posts/<post_id>/comment', methods=['POST'])
@login_required
@published_project_required
def create_comment(post_id: str) -> str:
    """
    Create a comment
    :param post_id: str
    :return: str
    """
    post = Post.query.get(post_id)

    log.info('Creating comment', {'user_id': g.user.id, 'post_id': post.id, 'comment_data': request.form})

    if 'body' in request.form:
        mentions = Mentions(request.form['body'])
        parent_comment_id = request.form.get('parent_comment_id')
        # Some weirdness going on with bad values trying to get added
        parent_comment_id = parent_comment_id if parent_comment_id and parent_comment_id.isnumeric() else None
        comment = Comment(body=mentions.body, parent_comment_id=parent_comment_id, user=g.user, post_id=post.id)

        post.comments.append(comment)
        db.session.commit()

        mentions.publish_comment(comment)
        challenge_factory('comment_created', {'comment': comment})
        notification_factory('comment_created', {'comment': comment}).publish()
    else:
        log.warn('Comment was empty', {'user_id': g.user.id, 'post_id': post.id})

    if request.headers.get('X-Requested-With') == 'fetch':
        partial = get_template_attribute('partials/comments.html', 'nested_comments')
        return partial(post.comments, True)
    else:
        return redirect(url_for('posts.show', post_id=post.url_slug))


@posts.route('/posts/<post_id>/comment/<comment_id>/delete')
@login_required
def delete_comment(post_id: str, comment_id: str) -> str:
    """
    Delete a comment
    :param post_id: str
    :param comment_id: str
    :return:
    """
    comment = Comment.query.get(comment_id)

    log.info('Deleting comment', {'post_id': post_id, 'comment_id': comment.id, 'user_id': g.user.id})

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
        partial = get_template_attribute('partials/comments.html', 'nested_comments')
        return partial(comment.post.comments, True)
    else:
        return redirect(url_for('posts.show', post_id=comment.post.url_slug))


@posts.route('/posts/<post_id>/comment/<comment_id>/edit', methods=['POST'])
@login_required
def edit_comment(post_id: str, comment_id: str) -> str:
    """
    Edit a comment
    :param post_id: str
    :param comment_id: str
    :return: str
    """
    comment = Comment.query.get(comment_id)

    log.info('Editing comment', {'post_id': post_id, 'comment_id': comment.id, 'user_id': g.user.id, 'comment_data': request.form})

    if comment.user.id == g.user.id:
        mentions = Mentions(request.form['body'])
        comment.body = mentions.body
        db.session.commit()
        mentions.publish_comment(comment)

    if request.headers.get('X-Requested-With') == 'fetch':
        partial = get_template_attribute('partials/comments.html', 'nested_comments')
        return partial(comment.post.comments, True)
    else:
        return redirect(url_for('posts.show', post_id=comment.post.url_slug))


@posts.route('/posts/<post_id>/vote')
@login_required
@published_project_required
def post_vote(post_id: str) -> str:
    """
    Vote on a post
    :param post_id: str
    :return: str
    """
    post = Post.query.get(post_id)
    size = request.args.get('size', 'lg')
    direction = request.args.get('direction', 'up')

    log.info('Voting post', {'user_id': g.user.id, 'post_id': post.id, 'direction': direction})

    if post.project.id != g.user.project.id:
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
    """
    Vote on a comment
    :param post_id: str
    :param comment_id: str
    :return: str
    """
    comment = Comment.query.get(comment_id)
    size = request.args.get('size', 'sm')
    direction = request.args.get('direction', 'up')

    log.info('Voting comment', {'user_id': g.user.id, 'comment_id': comment.id, 'direction': direction})

    if comment.user.project.id != g.user.project.id:
        comment.vote(g.user, direction)
        challenge_factory('comment_voted', {'comment': comment})
        notification_factory('comment_voted', {'comment': comment, 'direction': direction, 'voter': g.user}).publish()

    if request.headers.get('X-Requested-With') == 'fetch':
        partial = get_template_attribute('partials/vote.html', 'comment_vote')
        return partial(size, comment)
    else:
        return redirect(url_for('posts.show', post_id=post_id))


@posts.route('/posts/<post_id>/poll', methods=['POST'])
@login_required
@published_project_required
def answer_poll(post_id: str) -> str:
    """
    Response to a poll
    :param post_id: str
    :return: str
    """
    post = Post.query.get(post_id)
    choice = request.form.get('poll_choice')

    if choice:
        post.poll.answer(choice)
    else:
        log.warn('User did not submit an answer', {'user_id': g.user.id})

    return redirect(url_for('posts.show', post_id=post.url_slug))
