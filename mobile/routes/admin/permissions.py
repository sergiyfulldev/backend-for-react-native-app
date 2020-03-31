from flask import Blueprint, jsonify

from mobile.models import Permission, User

from mobile.utils import requires_permission

admin_permissions_blueprint = Blueprint('admin_permissions', __name__)

@admin_permissions_blueprint.route('/', methods=['GET'])
@requires_permission("admin")
def permissions():
    perms = Permission.query.all()

    if len(perms) == 0:
        return jsonify({
            'status': 'error',
            'message': 'No permissions to list'
        })

    _perms = []

    for perm in perms:
        _perms.append(perm.to_dict())

    return jsonify({
        'status': 'success',
        'message': '',
        'permissions': _perms
    })
