from flask import Blueprint, jsonify
from hackerstash.db import db
from hackerstash.models.user import User
from hackerstash.utils.auth import admin_api_key_required

api_admin = Blueprint('api_admin', __name__)


@api_admin.route('/api/admin/users/<user_id>', methods=['DELETE'])
@admin_api_key_required
def index(user_id):
    user = User.query.get(user_id)

    # Can't think of a way to cascade this at the db level
    if user.member and len(user.member.project.members) == 1:
        db.session.delete(user.member.project)

    db.session.delete(user)
    db.session.commit()

    return jsonify({'user_deleted': True}), 202
