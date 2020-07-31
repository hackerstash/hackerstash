from functools import wraps
from flask import g, request, redirect, url_for, render_template


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in g:
            return redirect(url_for('login.index', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def member_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in g or g.user.member.project.id != int(kwargs['project_id']):
            return render_template('projects/400.html')
        return f(*args, **kwargs)
    return decorated_function


def author_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in g:
            return redirect(url_for('leaderboard.index'))

        match = list(filter(lambda x: x.id == int(kwargs['post_id']), g.user.posts))
        if len(match) < 1:
            # TODO proper page
            return redirect(url_for('leaderboard.index'))
        return f(*args, **kwargs)
    return decorated_function
