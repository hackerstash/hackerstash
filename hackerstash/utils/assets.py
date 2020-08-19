from flask_assets import Environment, Bundle

assets = Environment()

styles = [
    'scss/main.scss'
]

scripts = [
    'js/admin.js',
    'js/avatar.js',
    'js/comments.js',
    'js/kanban.js',
    'js/menu.js',
    'js/messages.js',
    'js/modals.js',
    'js/posts.js',
    'js/previews.js',
    'js/projects.js',
    'js/recaptcha.js',
    'js/typeaheads.js',
    'js/votes.js'
]

js = Bundle(*scripts, output='out/main.js')
scss = Bundle(*styles, filters='pyscss', output='out/main.css', depends='**/*.scss')

assets.register('js_all', js)
assets.register('scss_all', scss)
