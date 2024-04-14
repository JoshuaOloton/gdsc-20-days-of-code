from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from .models import Permission, User

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()
            user = User.query.filter_by(name=current_user).first()
            if not user.can(permission):
                return jsonify({'error': 'Admin access required'}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator

def admin_required(f):
    return permission_required(Permission.ADMIN_ACCESS)(f)