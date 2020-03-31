from flask import Blueprint, request, jsonify

from mobile.models import User, Permission
from mobile.utils import validate_auth_token
from mobile.extensions import db


admin_users_blueprint = Blueprint('admin_users',__name__)

@admin_users_blueprint.route('/',methods=['GET'])
def users():
    users = User.query.all()

    user_data = []

    for user in users:
        user_data.append(user.to_dict())

    return jsonify({
        'status': 'success',
        'message': '',
        'users': user_data
    })

@admin_users_blueprint.route('/info/<uid>',methods=['GET'])
def user_info(uid):

    user = User.query.filter_by(id=uid).first()

    if user is None:
        return jsonify({
            'status': 'error',
            'message': 'Unable to locate user'
        })

    return jsonify({
        'status': 'success',
        'message': 'User information retrieved',
        'user': user.to_dict()
    })

@admin_users_blueprint.route('/permissions/',methods=['POST', 'DELETE'])
def user_permissions():
    _json = request.get_json()

    uid = _json.get('user_id')

    user = User.query.filter_by(id=uid).first()

    if user is None:
        return jsonify({
            'status': 'error',
            'message': 'Unable to locate user'
        })

    p_id = _json.get('permission_id')

    permission = Permission.query.filter_by(id=p_id).first()

    if permission is None:
        return jsonify({
            'status': 'error',
            'message': 'Invalid permission id'
        })

    #todo implement delete

    if request.method == "DELETE":
        user.permissions.remove(permission)
        db.session.add(user)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'Permission removed from the user'
        })

    elif request.method == "POST":
        user.permissions.append(permission)

        db.session.add(user)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'Permission added to user'
        })
