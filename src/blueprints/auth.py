from flask import Blueprint, jsonify, request
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                current_user,
                                jwt_required,
                                get_jwt_identity)
from models.users.user import User

# register blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.post('/register')
def register_user():
    data = request.get_json()
    user = User.get_user_by_username(username=data.get('username'))

    if user is not None:
        return jsonify({
            'error': 'User already exists'
        }), 403

    new_user = User(
        username=data.get('username'),
        email=data.get('email')
    )
    new_user.set_password(data.get('password'))

    try:
        new_user.save()
        return jsonify({
            'message': 'User created successfully'
        }), 201
    except Exception:
        return jsonify({
            'error': 'Error while creating the user'
        }), 500

@auth_bp.post('/login')
def login_user():
    data = request.get_json()
    user = User.get_user_by_username(username=data.get('username'))
    if user and user.check_password(password=data.get('password')):
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        return jsonify({
            'message': 'Logged in successfully',
            'token': {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        }), 200

    return jsonify({
        'error': 'Invalid username or passwrd'
    }), 400

@auth_bp.get('/whoami')
@jwt_required()
def whoami():
    return jsonify({
        'username': current_user.username,
        'email': current_user.email
    }), 200

@auth_bp.get('/refresh')
@jwt_required(refresh=True)
def refresh_access():
    identity = get_jwt_identity()
    return jsonify({
        'access_token': create_access_token(identity=identity)
    })
