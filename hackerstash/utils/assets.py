from flask_assets import Environment, Bundle

assets = Environment()

styles = [
    'scss/main.scss'
]

scripts = [
    'js/avatar.js'
]

js = Bundle(*scripts, output='out/main.js')
scss = Bundle(*styles, filters='pyscss', output='out/main.css')

assets.register('js_all', js)
assets.register('scss_all', scss)