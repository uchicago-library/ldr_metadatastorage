
from abc import ABCMeta, abstractmethod

class StorageSystem:
    """The abstract class for a storage system.

    Any inherited concrete class must implement
    1. find_root() -> return all second-level collections from the root collection
    2. find_specific_collection() -> take a collection identifier and
       return a list of identifiers below that collection
    3. find_extensions() -> take a collection identifier  and the base64 string for the proxy
       metadata that may be available for this collection
    4. find_collection_extensions() -> take a collection identifier and return a list
       of identifiers for proxy metadata that may be available for that collection.
    5. find_core_metadata() -> take a collection identifier and return key:value pairs for all
       descriptive metadata available for the collection
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def find_root(self):
        """return a list of strings or empty list

        return all second-level collections from the root collection
        """
        raise NotImplementedError

    @abstractmethod
    def find_specific_collection(self, identifier):
        """return a list of strings or empty list

        take a collection identifier and return a list of identifiers below
        that collection
        """
        raise NotImplementedError

    @abstractmethod
    def find_extension(self, extension):
        """returns base64 string or an empty string

        take a collection identifier  and the base64 string for the proxy
        metadata that may be available for this collection
        """
        raise NotImplementedError

    @abstractmethod
    def find_collection_extensions(self, collection_id):
        """returns a list of strings or an empty list

        take a collection identifier and return a list of identifiers
        for proxy metadata that may be available for that collection.

        """
        raise NotImplementedError

    @abstractmethod
    def find_core_metadata(self, collection_id):
        """returns a dict with ke:value pairs or None

        take a collection identifier and return key:value pairs for all
        descriptive metadata available for the collection
        """
        raise NotImplementedError