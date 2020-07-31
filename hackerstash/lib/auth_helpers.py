from functools import wraps
from flask import g, request, redirect, url_for


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login.index', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def member_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user.member.project.id != int(kwargs['project_id']):
            # TODO proper page
            return redirect(url_for('leaderboard.index'))
        return f(*args, **kwargs)
    return decorated_function


def author_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        match = list(filter(lambda x: x.id == int(kwargs['post_id']), g.user.posts))
        if len(match) < 1:
            # TODO proper page
            return redirect(url_for('leaderboard.index'))
        return f(*args, **kwargs)
    return decorated_function
