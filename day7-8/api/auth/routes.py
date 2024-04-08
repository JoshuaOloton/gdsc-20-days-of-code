from . import auth
from .. import bcrypt
from ..models import User
from api import db
from flask import jsonify, request
from flask_jwt_extended import create_access_token
from operator import itemgetter

@auth.route('/login', methods=['POST'])
def login():
    name, password = itemgetter('name', 'password')(request.json)
    user = User.query.filter_by(name=name).first()

    if user and user.verify_password(password):
        access_token = create_access_token(identity=name)
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token
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
