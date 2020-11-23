from flask import session, request, url_for, g, redirect, render_template
from werkzeug.exceptions import HTTPException
from hackerstash.lib.logging import Logging
from hackerstash.models.user import User
from hackerstash.utils.headers import Headers
from hackerstash.utils.page import Page

log = Logging(module='Hooks')


def init_app(app):
    @app.before_request
    def before_request_func() -> None:
        """
        A function that gets excecuted before every request
        :return: None
        """
        page = Page(request.path)

        # Don't want to be hitting the database for images and whatnot
        if page.static:
            return

        if 'id' in session:
            page = Page(request.path)
            g.user = User.query.get(session['id'])

            if not g.user:
                # Something is wrong with the user here
                log.warn('User had a session cookie but no user was found')
                session.pop('id', None)
                return redirect(url_for('auth.login'))

            if not g.user.username and not page.onboarding:
                return redirect(url_for('onboarding.index'))

    @app.after_request
    def after_request_func(response) -> None:
        """
        A function that is ran after every request
        :param response:
        :return: None
        """
        headers = Headers(response)
        return headers.set_cache_headers()

    @app.errorhandler(401)
    def unauthorized(_error: Exception):
        """
        Render the 401 page on an unauthorized error
        :param _error: Exception
        :return: str
        """
        return render_template('401.html'), 401

    @app.errorhandler(404)
    def page_not_found(_error: Exception):
        """
        Render the 404 page on an page_not_found error
        :param _error: Exception
        :return: str
        """
        return render_template('404.html'), 404

    @app.errorhandler(Exception)
    def handle_exception(error: Exception):
        """
        Render the 500 page on an handle_exception error
        :param error: Exception
        :return: str
        """
        if isinstance(error, HTTPException):
            return error
        log.error('Unhandled exception caught', error)
        return render_template('500.html'), 500
