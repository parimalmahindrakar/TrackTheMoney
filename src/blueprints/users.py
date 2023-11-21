from flask import Blueprint, jsonify, request
from models.users.user import User
from flask_jwt_extended import jwt_required
from models.users.user_schema import UserSchema

user_bp = Blueprint('user_bp', __name__)

@user_bp.get('/all')
@jwt_required()
def get_all_users():
  users = User.objects()
  result = UserSchema().dump(users, many=True)

  return jsonify({
    'users': result
  }), 200

