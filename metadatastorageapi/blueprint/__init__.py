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

from .storagelib.factory import StorageSystemFactory

BLUEPRINT = Blueprint('metadatastorageapi', __name__)
BLUEPRINT.config = {}
API = Api(BLUEPRINT)
LOG = logging.getLogger(__name__)

def _get_storage_system():
    from flask import current_app
    print(current_app.config.get("STORAGE_LOCATION"))
    return StorageSystemFactory(current_app.config.get("STORAGE_TYPE").lower(),
                                location=current_app.config.get("STORAGE_LOCATION")).build()

def _common_response_body_building(rtype="aggregate"):
        root = ElementTree.Element("{http://lib.uchicago.edu/ldr}output")
        request = ElementTree.SubElement(root, "{http://lib.uchicago.edu/ldr}request")
        request.text = "/"
        response_sent_timestamp = ElementTree.SubElement(root, "{http://lib.uchicago.edu/ldr}responseSentTimeStamp")
        response_sent_timestamp.text = datetime.now().isoformat()
        request_received_timestamp = ElementTree.SubElement(root, "{http://lib.uchicago.edu/ldr}requestReceivedTimeStamp")
        request_received_timestamp.text = datetime.now().isoformat()
        response_type = ElementTree.SubElement(root, "{http://lib.uchicago.edu/ldr}responseType")
        response_type.text = rtype
        response = ElementTree.SubElement(root, "{http://lib.uchicago.edu/ldr}response")
        metadata = ElementTree.SubElement(response, "{http://lib.uchicago.edu/ldr}metadata")
        return root, metadata

def _extension_response_body_building():
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
        extension = ElementTree.SubElement(response, "{http://lib.uchicago.edu/ldr}metadata")
        return root, extension

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
        storagesystem = _get_storage_system()
        collections = storagesystem.find_root()
        root, metadata = _common_response_body_building()
        for n_value in collections:
            has_part = ElementTree.SubElement(metadata, "{http://purl.org/dc/elements/1.1/}hasPart")
            has_part.set("{http://www.w3.org/2003/XMLSchema-instance}type", "dcterms:URI")
            has_part.text = "/collection/" + n_value
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
        storagesystem = _get_storage_system()
        collections = storagesystem.find_specific_collection(collection_identifier)
        root, metadata = _common_response_body_building()
        for n_value in collections:
            has_part = ElementTree.SubElement(metadata, "{http://purl.org/dc/elements/1.1/}hasPart")
            has_part.set("type", "URI")
            has_part.text = n_value
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
        storagesystem = _get_storage_system()
        core_metadata = storagesystem.find_core_metadata(collection_identifier)
        root, metadata = _common_response_body_building(rtype="atomic")
        for n in core_metadata:
            new = ElementTree.SubElement(metadata, n)
            val = core_metadata[n]['value']
            if 'http' in val:
                new.set("type", "URL")
            elif val[0] == "/":
                new.set("type", "URI")
            new.text = core_metadata[n]['value']
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

        root, metadata = _common_response_body_building()
        storagesystem = _get_storage_system()
        extensions = storagesystem.find_collection_extensions(collection_identifier)
        for n_value in extensions:
            rel = ElementTree.SubElement(metadata, "{http://purl.org/dc/elements/1.1/}relation")
            rel.set("type", "URI")
            rel.text = n_value
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
        storagesystem = _get_storage_system()
        extension = storagesystem.find_extension(extension_identifier)
        return APP.response_class(extension.encode("utf-8"), mimetype="text/plain;base64")

API.add_resource(Root, "/")
API.add_resource(Collection, "/collection/<string:collection_identifier>", methods=['GET', 'POST'])
API.add_resource(AllCollections, "/collections", methods=['GET'])
API.add_resource(ListForCollection, "/collections/<path:collection_identifier>", methods=['GET'])
API.add_resource(CollectionCore, "/collection/<string:collection_identifier>/core", methods=['GET'])
API.add_resource(ListCollectionProxies, "/collection/<string:collection_identifier>/proxies",
                 methods=['GET'])
API.add_resource(CollectionProxy,
                 "/collection/<string:collection_identifier>/proxies/<string:extension_identifier>",
                 methods=['GET'])
