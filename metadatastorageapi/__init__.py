"""an API to allow read and writ access to UChicago library metadata storage

"""

from flask import Flask
from .blueprint import BLUEPRINT
from flask_env import MetaFlaskEnv

class Configuration(metaclass=MetaFlaskEnv):
    ENV_PREFIX='DIGCOLL_RETRIEVER_'
    DEBUG = False
    DEFER_CONFIG = False


APP = Flask(__name__)

APP.config.from_object(Configuration)

APP.register_blueprint(BLUEPRINT)