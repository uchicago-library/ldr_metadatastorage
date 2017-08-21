from os import path
from xml.etree import ElementTree

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