# Import the libraries
from flask import Flask, jsonify
from os import environ
from config import config
from blueprints.users import user_bp
from blueprints.auth import auth_bp
from models.users.user import User
from blocklist import BLOCKLIST
import extensions

# set env
env = environ.get('TRACKTHEMONEY_ENV', 'local')

def create_app(config_name):
    # Flask app object
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # initialize the app with the extensions if required
    extensions.jwt.init_app(app)

    # register blueprints
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # load user from jwt token
    @extensions.jwt.user_lookup_loader
    def user_lookup_callback(__jwt_headers, jwt_data):
        return User.objects(id=jwt_data.get('sub')).first()

    # jwt error handlers
    @extensions.jwt.expired_token_loader
    def expire_token_callback(jwt_header, jwt_data):
        return jsonify({
            'message': 'Token has expired',
            'error': 'token_expired'
        }), 401

    @extensions.jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'message': 'Signature verfication failed',
            'error': 'invalid_token'
        }), 401

    @extensions.jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            'message': 'Request does not contain valid token',
            'error': 'authorization_header'
        }), 401

    # jwt blocklist for tokens
    @extensions.jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload.get('jti') in BLOCKLIST

    @extensions.jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'message': 'This token has been revoked',
            'error': 'token_revoked'
        }), 401

    return app

if env == 'test':
    app = create_app('test')
elif env == 'production':
    app = create_app('production')
else:
    app = create_app('development')
