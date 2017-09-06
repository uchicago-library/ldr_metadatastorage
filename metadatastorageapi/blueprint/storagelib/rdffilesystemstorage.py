
from rdflib import Graph, URIRef

class RDFFileSystemStorage(object):
    def __init__(self, file_path):
        self.graph = Graph().parse(file_path)

    def find_root_collections(self):
        root = URIRef("http://metadatastorage.lib.uchicago.edu/collection/ldr")
        [x for x in g.subjects() if x == root]