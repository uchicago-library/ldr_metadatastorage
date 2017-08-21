from os import path
from xml.etree import ElementTree

class FileSystemStorage(object):
    def __init__(self):
        self.filepath = path.realpath(path.join("../sandbox", "collections.xml"))
        self.data = ElementTree.parse(self.filepath)

    def find_a_particular_collection(self, identifier):
        match = self.data.getroot().find("{http://lib.uchicago.edu/ldr}collection/{http://purl.org/dc/elements/1.1}identifier=={}".format(identifier))
        print(match.parent())
