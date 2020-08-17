from flask import Blueprint, jsonify, request
from hackerstash.db import db
from hackerstash.lib.logging import logging
from hackerstash.models.user import User
from hackerstash.models.contest import Contest
from hackerstash.utils.auth import admin_api_key_required

api_admin = Blueprint('api_admin', __name__)


@api_admin.route('/api/admin/users/<user_id>', methods=['DELETE'])
@admin_api_key_required
def delete_user(user_id: str):
    user = User.query.get(user_id)

    # Can't think of a way to cascade this at the db level
    if user.member and len(user.member.project.members) == 1:
        db.session.delete(user.member.project)

    try:
        db.session.delete(user)
        db.session.commit()

        return jsonify({'status': 'Accepted'}), 202
    except Exception as e:
        logging.error('Failed to delete user %s', e)
        return jsonify({'status': 'Failed', 'error': str(e)}), 500


@api_admin.route('/api/admin/contests/end', methods=['POST'])
@admin_api_key_required
def end_contest():
    try:
        week = request.args.get('week')
        year = request.args.get('year')
        Contest.end(
            int(week) if week else None,
            int(year) if year else None
        )
        return jsonify({'status': 'Accepted'}), 202
    except Exception as e:
        logging.error('Failed to end contest %s', e)
        return jsonify({'status': 'Failed', 'error': str(e)}), 500
