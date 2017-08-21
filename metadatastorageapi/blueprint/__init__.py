"""the blueprint routes for the API
See spec section https://github.com/uchicago-library/ldr_metadatastorage/wiki#contract-for-available-endpoints
"""

from datetime import datetime
from io import BytesIO
import logging
from os import path
from urllib.parse import unquote
from xml.etree import ElementTree
from sys import stderr
from flask import Blueprint, Response, send_file
from flask_restful import Resource, Api, reqparse
from testlib.output import define_namespaces, build_envelope

from .storagelib.filesystemstorage import FileSystemStorage

BLUEPRINT = Blueprint('metadatastorageapi', __name__)
BLUEPRINT.config = {}
API = Api(BLUEPRINT)
LOG = logging.getLogger(__name__)

def _common_response_body_building():
        root = ElementTree.Element("{http://lib.uchicago.edu/ldr}output")
        request = ElementTree.SubElement(root, "{http://lib.uchicago.edu/ldr}request")
        request.text = "/"
        response_sent_timestamp = ElementTree.SubElement(root, "{http://lib.uchicago.edu/ldr}responseSentTimeStamp")
        response_sent_timestamp.text = datetime.now().isoformat()
        request_received_timestamp = ElementTree.SubElement(root, "{http://lib.uchicago.edu/ldr}requestReceivedTimeStamp")
        request_received_timestamp.text = datetime.now().isoformat()
        response_type = ElementTree.SubElement(root, "{http://lib.uchicago.edu/ldr}responseType")
        response_type.text = "aggregate"
        response = ElementTree.SubElement(root, "{http://lib.uchicago.edu/ldr}response")
        metadata = ElementTree.SubElement(response, "{http://lib.uchicago.edu/ldr}metadata")
        return root, metadata

class Root(Resource):
    """a class to hold methods to return root-level API functionality available

    has 1 method: get that takes no parameters
    """
    def get(self):
        """a method to return static root context;

        The output of this should never change. It is the equivalent of an un-changing
        index.html page.
        """
        from metadatastorageapi import APP
        root, metadata = _common_response_body_building()
        stderr.write(str(root))
        relation = ElementTree.SubElement(metadata, "{http://purl.org/dc/elements/1.1/}relation")
        relation.set("{http://purl.org/dc/terms/}type", "{http://purl.org/dc/terms/}URI")
        relation.text = "/collections"
        return APP.response_class(ElementTree.tostring(root), mimetype="application/xml")

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
        from metadatastorageapi import APP
        root, metadata = _common_response_body_building()
        relation_one = ElementTree.SubElement(metadata, "{http://purl.org/dc/elements/1.1/}relation")
        relation_one.set("{http://www.w3.org/2003/XMLSchema-instance}type", "{http://purl.org/dc/terms/}URI")
        relation_one.text = path.join("/", collection_identifier, "/core")
        relation_two = ElementTree.SubElement(metadata, "{http://purl.org/dc/elements/1.1/}relation")
        relation_two.set("{http://www.w3.org/2003/XMLSchema-instance}type", "{http://purl.org/dc/terms/}URI")
        relation_two.text = path.join("/", collection_identifier, "/extensions")
        return APP.response_class(ElementTree.tostring(root), mimetype="application/xml")

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
        from metadatastorageapi import APP
        collection = FileSystemStorage("sandbox/collections.xml").find_root()
        root, metadata = _common_response_body_building()
        parts = collection.findall("{http://purl.org/dc/elements/1.1/}hasPart")
        for n_value in parts:
            has_part = ElementTree.SubElement(metadata, "{http://purl.org/dc/elements/1.1/}hasPart")
            has_part.set("{http://www.w3.org/2003/XMLSchema-instance}type", "{http://purl.org/dc/terms/}URI")
            has_part.text = "/collection/" + n_value.text
        return APP.response_class(ElementTree.tostring(root), mimetype="application/xml")

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
        from metadatastorageapi import APP
        collection = FileSystemStorage("sandbox/collections.xml").find_specific_collection(collection_identifier)
        root, metadata = _common_response_body_building()
        parts = collection.findall("{http://purl.org/dc/elements/1.1/}hasPart")
        for n_value in parts:
            print(parts)
            has_part = ElementTree.SubElement(metadata, "{http://purl.org/dc/elements/1.1/}hasPart")
            has_part.set("{http://www.w3.org/2003/XMLSchema-instance}type", "{http://purl.org/dc/terms/}URI")
            has_part.text = n_value.text
        return APP.response_class(ElementTree.tostring(root), mimetype="application/xml")

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
        from metadatastorageapi import APP
        core_metadata = None # need to retrieve core metadata from database in order to insert as sub element of metadata in response
        root, metadata = _common_response_body_building()
        return APP.response_class(ElementTree.tostring(root), mimetype="application/xml")

class ListCollectionProxies(Resource):
    """a class to hold method for getting a list of any available extension metadata for a collection

    has 1 method: get that takes 1 parameter
    """
    def get(self, collection_identifier):
        """a method to return a list of extension metadata (if available) for a particular collection

        The output will be a response body that is metadata with at least one dc:relation xsi:type="dcterms:URI"
        for each extension metadata associated with the collection identified
        """
        from metadatastorageapi import APP
        extensions = [] # need to retrieve identifiers for all proxy metadata associated with a particular collection in order to add as relation elements in response
        root, metadata = _common_response_body_building()
        for n_value in extensions:
            relation = ElementTree.SubElement(metadata, "{http://purl.org/dc/elements/1.1/}relation")
            relation.set("{http://www.w3.org/2003/XMLSchema-instance}type", "{http://purl.org/dc/terms/}URI")
            relation.text = n_value
        return APP.response_class(ElementTree.tostring(root), mimetype="application/xml")

class CollectionProxy(Resource):
    """a class to hold method for getting a particular extension metadata for a particular unit

    has 1 method: get that takes 2 parameters
    """
    def get(self, collection_identifier, extension_identifier):
        """a method to return a particular extension for a collection

        The output will be a response body that is a text/base64 mimetype containing a base64 encoding of some proxy metadata
        """
        from metadatastorageapi import APP
        extension = None # need to find extension metadata base64 identified with collection and as extension_identiifer and return it as a string
        return APP.response_class(extension, mimetype="text/base64")

API.add_resource(Root, "/")
API.add_resource(Collection, "/collection/<string:collection_identifier>", methods=['GET', 'POST'])
API.add_resource(AllCollections, "/collections", methods=['GET'])
API.add_resource(ListForCollection, "/collections/<path:collection_identifier>", methods=['GET'])
API.add_resource(CollectionCore, "/collection/<string:collection_identifier>/core", methods=['GET'])
API.add_resource(ListCollectionProxies, "/collection/<string:collection_identifier>/proxies",
                 methods=['GET'])
API.add_resource(CollectionProxy,
                 "/collection/<string:collection_identifier>/proxy/<string:extension_identifier>",
                 methods=['GET'])
