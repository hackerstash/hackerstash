from flask import session, request, url_for, g, redirect, render_template
from werkzeug.exceptions import HTTPException
from hackerstash.lib.logging import logging, publish_slack_message
from hackerstash.lib.sidebar import Sidebar
from hackerstash.models.user import User


def init_app(app):
    @app.before_request
    def before_request_func():
        # Don't want to be hitting the database for images
        # and whatnot
        if request.path.startswith('/static'):
            return

        if 'id' in session:
            g.user = User.query.get(session['id'])

            if not g.user:
                # Something is wrong with the user here
                logging.warning('User had a session cookie but no user was found')
                session.pop('id', None)
                return redirect(url_for('auth.login'))

            if not g.user.username \
                    and request.path not in [url_for('users.new'), url_for('users.create')] \
                    and not request.path.startswith('/static'):
                return redirect(url_for('users.new'))

        sidebar = Sidebar()
        g.prize_pool = sidebar.prize_pool
        g.time_remaining = sidebar.time_remaining
        g.no_current_contest = sidebar.no_current_contest

    @app.after_request
    def after_request_func(response):
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'no-referrer-when-downgrade'
        return response

    @app.errorhandler(404)
    def page_not_found(_error):
        return render_template('404.html'), 404

    @app.errorhandler(Exception)
    def handle_exception(error):
        if isinstance(error, HTTPException):
            return error
        logging.stack(error)
        publish_slack_message(error)
        return render_template('500.html'), 500
