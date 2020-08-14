import requests
from flask import Blueprint, jsonify, request, session
from hackerstash.config import config
from hackerstash.lib.logging import logging

api_locations = Blueprint('api_locations', __name__)


@api_locations.route('/api/locations')
def index() -> str:
    try:
        query = request.args.get('q')

        # Just check the session exists rather than
        # using the @login_required decorator as we
        # don't want to query the database
        if not query or 'id' not in session:
            return jsonify([])

        params = {
            'input': query,
            'types': '(cities)',
            'key': config['google_api_key']
        }

        r = requests.get('https://maps.googleapis.com/maps/api/place/autocomplete/json', params=params)
        r.raise_for_status()
        response = r.json()

        locations = list(map(lambda x: x['description'], response['predictions']))
        return jsonify(locations)
    except Exception as e:
        logging.error('Failed to get location data %s', e)
        return jsonify([])
