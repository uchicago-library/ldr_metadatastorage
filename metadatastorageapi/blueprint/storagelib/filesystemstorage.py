from os import path
from xml.etree import ElementTree
from sys import stderr

class FileSystemStorage(object):
    def __init__(self, filepath):
        self.filepath = path.abspath(filepath)
        self.data_root = ElementTree.parse(self.filepath).getroot()

    def find_root(self):
        collections = self.data_root.findall("{http://lib.uchicago.edu/ldr}collection")
        for n in collections:
            if n.find("{http://purl.org/dc/elements/1.1/}identifier").text == 'root':
                return n

    def find_specific_collection(self, identifier):
        collections = self.data_root.findall("{http://lib.uchicago.edu/ldr}collection")
        for n in collections:
            if n.find("{http://purl.org/dc/elements/1.1/}identifier").text == identifier:
                return n
        return None

    def find_extension(self, collection, extension):
        collection = self.find_specific_collection(collection)
        if collection:
            collections = self.data_root.findall("{http://lib.uchicago.edu/ldr}collection")
            for n in collections:
                if n.find("{http://purl.org/dc/elements/1.1/}identifier").text == extension:
                    return n.find("{http://purl.org/dc/elements/1.1}description").text
        return None

    def find_collection_extensions(self, collection_id):
        collection = self.find_specific_collection(collection_id)
        if collection:
            return collection
        return None

    def find_core_metadata(self, collection_id):
        collection = self.find_specific_collection(collection_id)
        print(collection)
        if collection:
            return collection
        return None