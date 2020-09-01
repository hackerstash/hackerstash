import arrow
from flask import session, request, url_for, g, redirect, render_template
from werkzeug.exceptions import HTTPException
from hackerstash.lib.logging import logging, publish_slack_message
from hackerstash.models.contest import Contest
from hackerstash.models.project import Project
from hackerstash.models.user import User


# Apparently the humanized time that someone already
# figured out isn't good enough! It needs to read like
# the following:
# 1 week
# 6 days
# 5 days
# 4 days
# 3 days
# 2 days
# 23 hours
# 1 hour
# 59 mins
# 1 min
def get_remaining_tournament_time():
    now = arrow.utcnow()
    end_of_week = arrow.utcnow().ceil('week')
    diff = end_of_week - now
    hours = diff.total_seconds() // 3600
    minutes = (diff.total_seconds() % 3600) // 60

    if diff.days == 7:
        return '1 week'
    if diff.days > 1:
        return f'{diff.days} days'
    if hours > 0:
        return f'{int(hours)} hours'
    return f'{int(minutes)} mins'


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

        count = Project.query.filter_by(published=True).count() * 2
        contest = Contest.get_current()

        g.prize_pool = f'${count + contest.top_up}'
        g.time_remaining = get_remaining_tournament_time()

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
        publish_slack_message(error)
        if isinstance(error, HTTPException):
            return error
        logging.stack(error)
        return render_template('500.html'), 500
