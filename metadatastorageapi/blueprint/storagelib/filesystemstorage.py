from os import path
from xml.etree import ElementTree

class FileSystemStorage(object):
    def __init__(self, filepath):
        self.filepath = filepath
        self.data_root = ElementTree.parse(self.filepath).getroot()

    def find_a_particular_collection(self, identifier):
        match = self.data_root.find(
            "{http://lib.uchicago.edu/ldr}collection/{http://purl.org/dc/elements/1.1}identifier=={}".format(identifier))
        print(match.parent())

