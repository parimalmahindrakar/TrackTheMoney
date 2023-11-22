from flask import Blueprint, jsonify, request
from models.users.user import User
from flask_jwt_extended import jwt_required
from models.users.user_schema import UserSchema

user_bp = Blueprint('user_bp', __name__)

@user_bp.get('/all')
@jwt_required()
def get_all_users():
    # TODO: validate per_page and page, request arguments

    page = request.args.get('page', type=int)
    per_page = request.args.get('per_page', type=int)
    users = User.objects

    if page and per_page:
        selected_users = users.skip((page - 1) * per_page).limit(per_page)
        result = UserSchema().dump(selected_users, many=True)

        return jsonify({
          'users': result
        }), 200

    else:
        result = UserSchema().dump(users, many=True)

        return jsonify({
          'users': result,
          'users_count': users.count()
        }), 200
