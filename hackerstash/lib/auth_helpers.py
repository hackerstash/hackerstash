from functools import wraps
from flask import g, request, redirect, url_for, render_template
from werkzeug.exceptions import Unauthorized


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
            return render_template('projects/401.html')
        return f(*args, **kwargs)
    return decorated_function


def published_project_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user.member or not g.user.member.project.published:
            raise Unauthorized()
        return f(*args, **kwargs)
    return decorated_function


def author_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in g:
            return render_template('posts/401.html')

        match = list(filter(lambda x: x.id == int(kwargs['post_id']), g.user.posts))

        if len(match) < 1:
            return render_template('posts/401.html')
        return f(*args, **kwargs)
    return decorated_function
