# Import the libraries
from flask import Flask
from os import environ
from config import config
from blueprints.users import user_bp
# from blueprints.auth import auth_bp
import extensions

# set env
env = environ.get('TRACKTHEMONEY_ENV', 'local')

def create_app(config_name):
    # Flask app object
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # register blueprints
    app.register_blueprint(user_bp, url_prefix='/users')
    # app.register_blueprint(auth_bp, url_prefix='/auth')

    return app

if env == 'test':
    app = create_app('test')
elif env == 'production':
    app = create_app('production')
else:
    app = create_app('development')
