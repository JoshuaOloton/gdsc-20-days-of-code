from . import admin
from flask_jwt_extended import jwt_required
from ..decorators import admin_required

@admin.route('/earnings', methods=['GET'])
@jwt_required()
@admin_required
def earnings():
    return 'Admin access granted'