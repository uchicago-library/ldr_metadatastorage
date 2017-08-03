"""the blueprint routes for the API
See spec section https://github.com/uchicago-library/ldr_metadatastorage#contract-for-available-endpoints
"""

from io import BytesIO
import logging
from urllib.parse import unquote
from xml.etree import ElementTree

from testlib.output import define_namespaces, build_envelope
from flask import Blueprint, send_file
from flask_restful import Resource, Api, reqparse

BLUEPRINT = Blueprint('metadatastorageapi', __name__)
BLUEPRINT.config = {}
API = Api(BLUEPRINT)

LOG = logging.getLogger(__name__)

class Root(Resource):
    """a class to hold methods to return root-level API functionality available

    has 1 method: get that takes no parameters
    """
    def get(self):
        """a method to return static root context;

        The output of this should never change. It is the equivalent of an un-changing
        index.html page.
        """
        temp_file = BytesIO()

        return {"value": "not implemented"}

class AllCollections(Resource):
    """a class to hold method for getting list of collections in system

    has 1 method: get that takes no parameters
    """
    def get(self):
        """a method to return list of all root-level collections available

        The output will have a response body that is metadata with at least one
        dc:hasPart xsi:type="dcterms:URI". The value of each dc:relation will
        be resolvable to a collection.
        """
        temp_file = BytesIO()
        root = build_envelope("{http://lib.uchicago.edu/ldr}output")
        tree = ElementTree.parse(root)
        return {"value": "not implemented"}

class ListForCollection(Resource):
    """a class to hold methods for getting a collection or posting a new collection

    has 1 method: get that takes 1 parameter
    """
    def get(self, collection_identifier):
        """a method to return all collections available from the hierarchy level of collection_identifier

        The output will be a response body that is metadata with at least one
        dc:hasPart xsi:type="dcterms:URI" or xsi:type="dcterms:URL".
        The value of each dc:hasPart will be resolvable to a collection or an asset
        """
        return {"value": "not implemented"}

class Collection(Resource):
    """a class to hold methods for getting a collection or posting a new collection

    has 2 methods: get and post that booth take one parameter
    """
    def get(self, collection_identifier):
         """a method to return all endpoints available from a specific collection

        The output will be a response body that is metadata with at least one
        dc:hasPart xsi:type="dcterms:URI" or xsi:type="dcterms:URL".
        The value of each dc:hasPart will be resolvable to a collection or an asset
        """
        return {"value": "not implemented"}

    def post(self, collection_identifier):
        return {"value": "not implemented"}

class CollectionCore(Resource):
    """a class to hold method for getting core metadata for a particular collection

    has 1 method: get that takes 1 parameter
    """
    def get(self, collection_identifier):
        """a method to return the core metadata available for a particular collection

        The output will be a response body that is metadata with
        - 1 dc:title
        - 1 dc:identifier
        - in addition, it may have dc:relation xsi:type="dcterms:URI", and/or dc:hasPart xsi:type="dcterms:URI|dcterms:URL"
        and/or dc:isPartOf xsi:type="dcterms:URI"
        """
        return {"value": "not implemented"}

class ListCollectionExtensions(Resource):
    """a class to hold method for getting a list of any available extension metadata for a collection

    has 1 method: get that takes 1 parameter
    """
    def get(self, collection_identifier):
        """a method to return a list of extension metadata (if available) for a particular collection

        The output will be a response body that is metadata with at least one dc:relation xsi:type="dcterms:URI"
        for each extension metadata associated with the collection identified
        """
        return {"value": "not implemented"}

class CollectionExtension(Resource):
    """a class to hold method for getting a particular extension metadata for a particular unit

    has 1 method: get that takes 2 parameters
    """
    def get(self, collection_identifier, extension_identifier):
        """a method to return a particular extension for a collection

        The output will be a response body that is extension with an element type, name, and data
        where type is the format (text, json or xml) of the extension metadata, name is the unique identifier
        for the extension metadata in context of the collection being extended and the data contains the
        extension metadata
        """
        return {"value": "not implemented"}

API.add_resource(Root, "/")
API.add_resource(AllCollections, "/collections", methods=['GET'])
API.add_resource(ListForCollection, "/collections/<path:collection_identifier>", methods=['GET'])
API.add_resource(Collection, "/collection/<string:collection_identifier>", methods=['GET', 'POST'])
API.add_resource(CollectionCore, "/collection/<string:collection_identifier>/core", methods=['GET'])
API.add_resource(ListCollectionExtensions, "/collection/<string:collection_identifier>/extensions", methods=['GET'])
API.add_resource(CollectionExtension, "/collection/<string:collection_identifier>/extensions/<string:extension_identifier>", methods=['GET'])