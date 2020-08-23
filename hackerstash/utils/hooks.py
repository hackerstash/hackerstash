import arrow
from datetime import datetime
from flask import session, request, url_for, g, redirect, render_template
from hackerstash.lib.logging import logging
from hackerstash.models.contest import Contest
from hackerstash.models.user import User
from hackerstash.models.project import Project


def init_app(app):
    @app.before_request
    def before_request_func():
        if 'id' in session:
            g.user = User.query.get(session['id'])

            if not g.user.username \
                    and request.path not in [url_for('users.new'), url_for('users.create')] \
                    and not request.path.startswith('/static'):
                return redirect(url_for('users.new'))

        count = Project.query.filter_by(published=True).count() * 2
        contest = Contest.get_current()

        g.prize_pool = f'${count + contest.top_up}.00'
        g.time_remaining = arrow.utcnow().ceil('week').humanize(only_distance=True)

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

    @app.errorhandler(500)
    def internal_server_error(error):
        logging.error('Internal server error %s', str(error))
        return render_template('500.html'), 500
