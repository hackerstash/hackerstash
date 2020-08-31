import json

import arrow
import requests
from flask import session, request, url_for, g, redirect, render_template
from werkzeug.exceptions import HTTPException

from hackerstash.config import config
from hackerstash.lib.logging import logging
from hackerstash.models.contest import Contest
from hackerstash.models.project import Project
from hackerstash.models.user import User


def init_app(app):
    @app.before_request
    def before_request_func():
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

    @app.errorhandler(Exception)
    def handle_exception(error):
        try:
            if config['app_environment'] == 'live':
                url = "https://hooks.slack.com/services/" + config['error_webhook']
                payload = {
                    "username": "500 Error",
                    "icon_emoji": ":octagonal_sign:",
                    "attachments": [
                        {
                            "color": "danger",
                            "text": str(error)
                        }
                    ]
                }
                headers = {
                    'Content-Type': 'application/json'
                }
                requests.request("POST", url, headers=headers, data=json.dumps(payload))
        finally:
            if isinstance(error, HTTPException):
                return error
            logging.stack(error)
            return render_template('500.html'), 500
