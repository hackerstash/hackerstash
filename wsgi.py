from hackerstash.server import create_app

app = create_app()


# Should fix issues with flask_dance thinking it's http in prod
# https://flask.palletsprojects.com/en/1.1.x/deploying/wsgi-standalone/#deploying-proxy-setups
class CustomProxyFix(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        host = environ.get('HTTP_X_FHOST', '')
        if host:
            environ['HTTP_HOST'] = host
        return self.app(environ, start_response)


app.wsgi_app = CustomProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
