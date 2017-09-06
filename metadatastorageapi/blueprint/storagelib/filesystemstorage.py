from os import path
from sys import stderr
from xml.etree import ElementTree

from .storagesystem import StorageSystem

class FileSystemStorage(StorageSystem):
    def __init__(self, filepath):
        self.filepath = path.abspath(filepath)
        self.data_root = ElementTree.parse(self.filepath).getroot()

    def _match_collection(self, collection="root"):
        collections = [x for x in self.data_root.findall("{http://lib.uchicago.edu/ldr}collection") if x.find("{http://purl.org/dc/elements/1.1/}identifier").text == collection]
        if len(collections) == 1:
            return collections[0]
        return None

    def _find_subcollections(self, collection):
        sub_collections = [x for x in collection.findall("{http://purl.org/dc/elements/1.1/}hasPart")]
        output = []
        for x in sub_collections:
            output.append(x.text)
        return output

    def _get_list_of_extensions(self, collection_id):
        match = self._match_collection(collection=collection_id)
        output = []
        extensions = [x for x in match.findall("{http://purl.org/dc/elements/1.1/}relation")]
        output = []
        for ext in extensions:
            output.append(ext.text)
        return output

    def find_root(self):
        match = self._match_collection()
        return self._find_subcollections(match)

    def find_specific_collection(self, identifier):
        match = self._match_collection(collection=identifier)
        return self._find_subcollections(match)

    def find_extension(self, extension):
        collection = self._match_collection(collection=extension)
        return collection.find("{http://purl.org/dc/elements/1.1/}description").text

    def find_collection_extensions(self, collection_id):
        return self._get_list_of_extensions(collection_id)

    def find_core_metadata(self, collection_id):
        collection = self._match_collection(collection=collection_id)
        output = {}
        for element in collection:
            tag_name = element.tag
            value = element.text
            output[tag_name] = {'value':value}
        return output
