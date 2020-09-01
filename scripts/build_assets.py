from hackerstash.server import app
from hackerstash.lib.logging import logging
from hackerstash.utils.assets import assets, js, scss

if __name__ == '__main__':
    with app.app_context():
        assets.init_app(app)
        for asset in [js, scss]:
            asset.build()
        logging.info('Assets built successfully')
