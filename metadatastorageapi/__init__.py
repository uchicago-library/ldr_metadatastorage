"""an API to allow read and writ access to UChicago library metadata storage

"""

from flask import Flask
from flask_env import MetaFlaskEnv

from .blueprint import BLUEPRINT

class Configuration(metaclass=MetaFlaskEnv):
    ENV_PREFIX='MSAPI_'
    DEBUG = False
    DEFER_CONFIG = False

APP = Flask(__name__)
APP.config.from_object(Configuration)
APP.register_blueprint(BLUEPRINT)