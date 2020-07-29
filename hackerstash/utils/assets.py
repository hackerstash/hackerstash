from flask_assets import Environment, Bundle

assets = Environment()

scss = Bundle('scss/main.scss', filters='pyscss', output='out/main.css')

assets.register('scss_all', scss)
