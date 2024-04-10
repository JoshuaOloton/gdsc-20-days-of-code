from . import auth
from .. import bcrypt
from ..models import User
from api import db
from datetime import datetime, timedelta
from flask import jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from operator import itemgetter

@auth.route('/login', methods=['POST'])
def login():
    name, password = itemgetter('name', 'password')(request.json)
    user = User.query.filter_by(name=name).first()

    if user and user.verify_password(password):
        access_token = create_access_token(identity=name, fresh=timedelta(minutes=15))
        refresh_token = create_refresh_token(identity=name)
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401


@auth.route('/register', methods=['POST'])
def register():
    name, password = itemgetter('name', 'password')(request.json)
    user = User.query.filter_by(name=name).first()
    
    # Check if user already exists
    if user:
        return jsonify({'error': 'User already exists'}), 400
    
    user = User(
        name=name,
        password=password
    )

    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201


@auth.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user, fresh=False)
    return jsonify({'access_token': access_token}), 200


@auth.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    username = get_jwt_identity()
    return jsonify(logged_in_as=username), 200