
from rdflib import Graph, URIRef, Namespace
from rdflib.namespace import RDF

from .storagesystem import StorageSystem

class RDFFileSystemStorage(StorageSystem):
    def __init__(self, file_path):
        self._namespaces = {"dc":Namespace("http://purl.org/dc/elements/1.1/"),
                            "dcterms":Namespace("http://purl.org/dc/terms/"),
                            "ldr":Namespace("http://lib.uchicago.edu/ldr/")}
        self._graph = Graph().parse(file_path)

    def find_root(self):
        root = URIRef(self._namespaces["ldr"]["ldr"])
        print(root)
        query = self._graph.query(
            """SELECT DISTINCT ?aname ?bname
            WHERE {
                ?a dc:isPartOf "ldr".
            }
            """
        )
        print(query)
        raise NotImplementedError

    def find_specific_collection(self, identifier):
        raise NotImplementedError

    def find_extension(self, extension):
        raise NotImplementedError

    def find_collection_extensions(self, collection_id):
        raise NotImplementedError

    def find_core_metadata(self, collection_id):
        raise NotImplementedError