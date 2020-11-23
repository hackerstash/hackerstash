from functools import wraps
from flask import g, request, redirect, url_for, render_template
from werkzeug.exceptions import Unauthorized
from hackerstash.config import config
from hackerstash.lib.logging import Logging
from hackerstash.utils.helpers import find_in_list

log = Logging(module='Auth')


def login_required(f):
    """
    A decorator that checks that a user exists in this request
    :param f: function
    :return: function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        logging_info = {'path': request.path, 'type': 'login_required'}

        if 'user' not in g:
            log.warn('Auth failure', {'reason': 'User has no session', **logging_info})
            return redirect(url_for('auth.login', next=request.url))

        return f(*args, **kwargs)
    return decorated_function


def member_required(f):
    """
    A decorator that checks that a user is a member of this project
    :param f: function
    :return: function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        logging_info = {'path': request.path, 'type': 'member_required', 'project_id': int(kwargs['project_id'])}

        if 'user' not in g:
            log.warn('Auth failure', {'reason': 'User has no session', **logging_info})
            return render_template('projects/401.html')

        if not g.user.admin and g.user.project.id != int(kwargs['project_id']):
            log.warn('Auth failure', {'reason': 'Not member of project', 'user_id': g.user.id, **logging_info})
            return render_template('projects/401.html')

        return f(*args, **kwargs)
    return decorated_function


def published_project_required(f):
    """
    A decorator that checks that a user has a published project
    :param f: function
    :return: function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        logging_info = {'path': request.path, 'type': 'published_project_required'}

        if not g.user.admin:
            if not g.user.project:
                log.warn('Auth failure', {'reason': 'Not member of project', 'user_id': g.user.id, **logging_info})
                raise Unauthorized()

            if not g.user.project.published:
                log.warn('Auth failure', {'reason': 'Project not published', 'user_id': g.user.id, **logging_info})
                raise Unauthorized()

        return f(*args, **kwargs)
    return decorated_function


def author_required(f):
    """
    A decorator that checks that a user is the author of this post
    :param f: function
    :return: function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        logging_info = {'path': request.path, 'type': 'author_required', 'post_id': int(kwargs['post_id'])}

        if 'user' not in g:
            log.warn('Auth failure', {'reason': 'User has no session', **logging_info})
            return render_template('posts/401.html')

        post = find_in_list(g.user.posts, lambda x: x.id == int(kwargs['post_id']))

        if not post:
            log.warn('Auth failure', {'reason': 'user is not author of post', 'user_id': g.user.id, **logging_info})
            return render_template('posts/401.html')

        return f(*args, **kwargs)
    return decorated_function


def admin_api_key_required(f):
    """
    A decorator that checks that the admin api is given
    :param f: function
    :return: function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        logging_info = {'path': request.path, 'type': 'admin_api_key_required'}

        if 'x-api-key' not in request.headers:
            log.warn('Auth failure', {'reason': 'Api key missing', **logging_info})
            raise Unauthorized()

        if request.headers['x-api-key'] != config['admin_api_key']:
            log.warn('Auth failure', {'reason': 'Api key incorrect', **logging_info})
            raise Unauthorized()

        return f(*args, **kwargs)
    return decorated_function


def admin_login_required(f):
    """
    A decorator that checks that a user is an admin
    :param f: function
    :return: function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        logging_info = {'path': request.path, 'type': 'admin_login_required'}

        if 'user' not in g:
            log.warn('Auth failure', {'reason': 'User has no session', **logging_info})

        if not g.user.admin:
            log.warn('Auth failure', {'reason': 'User is not admin', **logging_info})
            return redirect(url_for('home.index'))

        return f(*args, **kwargs)
    return decorated_function
