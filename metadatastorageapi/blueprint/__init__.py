"""the blueprint routes for the API

1. / = returns the endpoints available at the root of the API
1. /units = returns a list of all collections in the ldr metadata storage
1. /units/[collection identifier/sub-collection identifier/sub-sub collection identifier] = returns a list of intellectual units that are part of a particular collection
1. /units = returns a list of intellectual units in the ldr metadata storage
1. /units/[intellectual unit identifier] = returns the endpoints available for a particular intellectual unit
1. /units/[intellectual unit identifier]/core = returns the core (metadata) describing a particular intellectual unit
1. /units/[intellectual unit identifier]/extensions = returns a list of extension (metadata) that are available for a particular intellectual unit
1. /units/[intellectual unit identifier]/extensions/[extension identifier] = returns the extension (metadata) identified by extension identifier that is available for intellectual unit unit identifier

"""
import logging
from urllib.parse import unquote

from flask import Blueprint
from flask_restful import Resource, Api, reqparse

BLUEPRINT = Blueprint('metadatastorageapi', __name__)
BLUEPRINT.config = {}
API = Api(BLUEPRINT)

LOG = logging.getLogger(__name__)

class Root(Resource):
    def get(self):
        return "not implemented"

class Collections(Resource):
    def get(self):
        return "not implemented"

    def post(self):
        return "not implemented"

class Units(Resource):
    def get(self, collection_identifier):
        return "not implemented"

class Unit(Resource):
    def get(self, unit_identifier):
        return "not implemented"

class UnitCore(Resource):
    def get(self, unit_identifier):
        return "not implemented"

class UnitExtensions(Resource):
    def get(self, unit_identifier):
        return "not implemented"

class Extension(Resource):
    def get(self, unit_identifier, extension_identifier):
        return "not implemented"

API.add_resource(Root, "/")
API.add_resource(Collections, "/units/")
API.add_resource(Units, "/units/<path:collection_identifier>/")
API.add_resource(Unit, "/unit/<string:unit_identifier>/")
API.add_resource(UnitCore, "/unit/<string:unit_identifier>/core/")
API.add_resource(UnitExtensions, "/unit/<string:unit_identifier>/extensions/")
API.add_resource(Extension, "/unit/<string:unit_identifier>/extensions/<string:extension_identifier>/")