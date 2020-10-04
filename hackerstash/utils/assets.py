from flask_assets import Environment, Bundle

assets = Environment()

# We may want to set this if we keep getting weird 404s due to the assets
# assets.auto_build = config['app_environment'] == 'production'

styles = [
    'scss/main.scss'
]

scripts = [
    'js/admin.js',
    'js/avatar.js',
    'js/comments.js',
    'js/confetti.js',
    'js/editor.js',
    'js/home.js',
    'js/menu.js',
    'js/messages.js',
    'js/modals.js',
    'js/notifications.js',
    'js/pagination.js',
    'js/previews.js',
    'js/projects.js',
    'js/recaptcha.js',
    'js/toast.js',
    'js/typeaheads.js',
    'js/votes.js'
]

js = Bundle(*scripts, output='out/main.js')
scss = Bundle(*styles, filters='libsass', output='out/main.css', depends='**/*.scss')

assets.register('js_all', js)
assets.register('scss_all', scss)
