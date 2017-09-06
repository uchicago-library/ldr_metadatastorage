from .rdffilesystemstorage import RDFFileSystemStorage
from .filesystemstorage import FileSystemStorage

class StorageSystemFactory(object):
    def __init__(self, product_name, location=None):
        self._request = product_name
        self._filepath = location

    def build(self):
        """a method to return the appropriate storage system to return the queries
        """
        if self._request == 'xml-filesystem':
            return FileSystemStorage(self._filepath)
        elif self._request == 'rdf-filesystem':
            return RDFFileSystemStorage(self._filepath)
        else:
            raise ValueError("{} is not a valid request to the StorageSystemFactory.".format(self._request))