
from rdflib import Graph, URIRef

from .storagesystem import StorageSystem

class RDFFileSystemStorage(StorageSystem):
    def __init__(self, file_path):
        self.graph = Graph().parse(file_path)

    def find_root_collections(self):
        root = URIRef("http://metadatastorage.lib.uchicago.edu/collection/ldr")
        [x for x in g.subjects() if x == root]
        return []

    def find_specific_collection(self, identifier):
        return []

    def find_extension(self, extension):
        return None

    def find_collection_extensions(self, collection_id):
        return []

    def find_core_metadata(self, collection_id):
        return {}
