from flask import Blueprint, jsonify, request
from hackerstash.lib.universal_search import universal_search
from hackerstash.utils.auth import login_required

search = Blueprint('search', __name__)


@search.route('/search')
@login_required
def index() -> str:
    response = universal_search(request.args.get('q'))
    return jsonify(response)
