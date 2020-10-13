from hackerstash.server import app
from hackerstash.lib.logging import Logging
from hackerstash.utils.assets import assets, js, scss

log = Logging(module='Scripts::Assets')

if __name__ == '__main__':
    with app.app_context():
        assets.init_app(app)
        for asset in [js, scss]:
            asset.build()
        log.info('Assets built successfully')
