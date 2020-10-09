import json
from flask import Blueprint, jsonify, request
from hackerstash.lib.logging import logging
from hackerstash.lib.webhooks.factory import webhook_factory
from hackerstash.models.contest import Contest
from hackerstash.utils.auth import admin_api_key_required

api_admin = Blueprint('api_admin', __name__)


# TODO: DEPRECATED
@api_admin.route('/api/admin/contests/end', methods=['POST'])
@admin_api_key_required
def end_contest():
    logging.info('Ending the contest via the admin API')
    try:
        week = request.args.get('week')
        year = request.args.get('year')
        Contest.end(
            int(week) if week else None,
            int(year) if year else None
        )
        return jsonify({'status': 'Accepted'}), 202
    except Exception as e:
        logging.stack(e)
        return jsonify({'status': 'Failed', 'error': str(e)}), 500


@api_admin.route('/api/admin/webhook', methods=['POST'])
@admin_api_key_required
def webhook():
    logging.info('Handling admin webhook')
    try:
        request_data = json.loads(request.data or '{}')
        event_type = request_data.get('type')
        event_data = request_data.get('data', {})
        webhook_factory(event_type, event_data)
        return jsonify({'status': 'Accepted'}), 202
    except Exception as e:
        logging.stack(e)
        return jsonify({'status': 'Failed', 'error': str(e)}), 500
