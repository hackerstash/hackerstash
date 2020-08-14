from datetime import datetime
from flask import session, request, url_for, g, redirect, render_template
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

        now = datetime.now()
        count = Project.query.count() * 10

        g.prize_pool = f'${count}.00'
        g.time_remaining = f'{6 - now.weekday()} days'

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
