from flask import Blueprint, jsonify, request, render_template
from hackerstash.lib.universal_search import universal_search
from hackerstash.utils.auth import login_required

search = Blueprint('search', __name__)


@search.route('/search')
@login_required
def index() -> str:
    results = universal_search(request.args.get('q'))
    if request.headers.get('X-Requested-With') == 'fetch':
        return jsonify(results)
    else:
        return render_template('search/index.html', results=results)
