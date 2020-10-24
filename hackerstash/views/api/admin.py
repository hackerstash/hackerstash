import json
from flask import Blueprint, jsonify, request
from hackerstash.lib.logging import Logging
from hackerstash.lib.webhooks.factory import webhook_factory
from hackerstash.utils.auth import admin_api_key_required

log = Logging('Views::Api::Admin')
api_admin = Blueprint('api_admin', __name__)


@api_admin.route('/api/admin/webhook', methods=['POST'])
@admin_api_key_required
def webhook():
    try:
        request_data = json.loads(request.data or '{}')
        log.info('Handling admin webhook', {'request_data': request_data})
        event_type = request_data.get('type')
        event_data = request_data.get('data', {})
        webhook_factory(event_type, event_data)
        return jsonify({'status': 'Accepted'}), 202
    except Exception as e:
        log.error('Failed to handle admin webhook', e)
        return jsonify({'status': 'Failed', 'error': str(e)}), 500
