from . import auth
from app.models import User, Role
from app import db
from datetime import datetime, timedelta
from flask import jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required


@auth.route('/login', methods=['POST'])
def login():
    name = request.json.get('name')
    password = request.json.get('password')

    if not name or not password:
        return jsonify({'error': 'Missing name or password'}), 400

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
    name = request.json.get('name')
    password = request.json.get('password')
    role = request.json.get('role')

    if not name or not password:
        return jsonify({'error': 'Missing name or password'}), 400
    if not role:
        return jsonify({'error': 'Missing role'}), 400

    # Check if user already exists
    user = User.query.filter_by(name=name).first()
    if user:
        return jsonify({'error': 'User already exists'}), 400
    
    role_id = 1 if role.strip().lower() == 'admin' else 2 if role.strip().lower() == 'user' else None
    if role_id is None:
        return jsonify({'error': 'Invalid role. Valid roles include \'User\' or \'Admin\''}), 400

    user = User(
        name=name,
        password=password,
        role_id=role_id
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