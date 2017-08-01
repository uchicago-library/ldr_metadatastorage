"""the module containing unit test code for the metadata storage api
"""

from datetime.datetime import now
from json import load, dumps
from xml.etree import ElementTree
import unittest

from metadatastorageapi import APP
from metadatastorageapi.output import create_output_xml, create_input_xml
class TestToSpecOnePointO(unittest.TestCase):
    """the api test suite
    """
    def setUp(self):
        self.app = APP.test_client()

    def tearDown(self):
        pass

    def _response_200(self, rv):
        self.assertEqual(rv.status_code, 200)

    def _create_complex_unit_xml_input(self):
        ElementTree.register_namespace("ldr", "http://lib.uchicago.edu/ldr")
        ElementTree.register_namespace("dc", "http://purl.org/dc/elements/1.1/")
        ElementTree.register_namespace("dcterms", "http://purl.org/dc/terms/")
        ElementTree.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")
        root = ElementTree.Element("input")
        requestSent = ElementTree.SubElement(root, "responseSentTimeStamp")
        requestSent.text = now().iso8601()
        core = ElementTree.SubElement(root, "core")
        metadata = ElementTree.SubElement(core, "metadata")
        title = ElementTree.SubElement(metadata, 'dc:title')
        title.text = "A Simple Title"
        date = ElementTree.SubElement(metadata, 'dc:date')
        date.text = "1800"
        relation_one = ElementTree.SubElement(metadata, 'dc:relation')
        relation_one.text = "testcollection"
        relation_two = ElementTree.SubElement(metadata, 'dc:relation')
        relation_two.text = "secondtestcollection"
        identifier = ElementTree.SubElement(metadata, 'dc:identifier')
        identifier.set("xsi:type", "URL")
        identifier.text = "https://dummyimage.com/200x300&text=test image!"
        return root


    def _create_json_output(self):
        return "not implemented"

    def test_rootURL(self):
        """tests whether there is a root url defined in blueprint
        """
        get = self.app.get("/")
        return self._response_200(get)

    def test_CollectionsURL(self):
        """tests whether there is a collections url defined in the blueprint
        """
        get = self.app.get("/units/")
        return self._response_200(get)

    def test_zeroDepthCollectionURL(self):
        """tests whether the units url in the blueprint takes a single directory
        """
        get = self.app.get("/units/{}/".format("foo"))
        return self._response_200(get)

    def test_nestedCollectionURL(self):
        """tests whether the units url in the blueprint takes multi directories
        """
        get = self.app.get("/units/{}/{}/".format("foo", "bar"))
        return self._response_200(get)

    def test_unitURL(self):
        """tests whether there is a unit getter url defined in blueprint
        """
        get = self.app.get("unit/{}/".format("foo"))
        return self._response_200(get)

    def test_coreURL(self):
        """tests whether there is a core getter url defined in blueprint
        """
        get = self.app.get("/unit/{}/core/".format("foo"))
        return self._response_200(get)

    def test_extensionsURL(self):
        """tests whether there is a extension listing url defined in blueprint
        """
        get = self.app.get("/unit/{}/extensions/".format("foo"))
        return self._response_200(get)

    def test_anExtensionsURL(self):
        """tests whether there is a extensions selection url defined in blueprint
        """
        get = self.app.get("/unit/{}/extensions/{}/".format("foo", "bar"))
        return self._response_200(get)


    def test_wellformed_units_get(self):
        """tests whether the api is returning a list of collections according to spec

        this tests the /units endpoint
        """
        return self.assertTrue(False)

    def test_wellformed_units_get_with_collection(self):
        """tests whether the api is returning a list of units in a particular collection according to spec

        this tests the /units/[collection identifier/sub-colletion identifier/sub-sub collection identifier]
        """
        return self.assertTrue(False)

    def test_post_new_collection(self):
        """test whether the api accepts good post input to create a new collection

        this tests the /units/[collection identifier] post method
        """
        return self.assertTrue(False)

    def test_wellformed_unit_get(self):
        """tests whether the api returns list of endpoints available to a unit

        this tests the GET /unit/[intellectual unit identifier] endpoint
        """
        return self.assertTrue(False)

    def test_post_new_unit(self):
        """tests whether the api accepts well-formed post data to create a new intellectual unit

        this tests the POST method on the /unit/[intellectual unit] endpoint
        """
        return self.assertTrue(False)

    def test_wellformed_core(self):
        """tests whether the api returns core metadata according to spec

        this tests the GET method on the /unit/[intellectual unit identifier]/core endpoint
        """
        return self.assertTrue(False)

    def test_wellformed_extension_list_get(self):
        """tests whether the api returns a list of extensions for a unit according to spec

        this tests the GET method on the /unit/[intellectual unit identifier]/extensions endpoint
        """
        return self.assertTrue(False)

    def test_wellformed_extension_get(self):
        """tests whether the api returns a particular extensions for a unit according to spec

        this tests the GET method on the /unit/[intellectual unit identifier]/extensions/[extension identifier] endpoint
        """
        get = self.app.get("/unit/test/extensions/extramdone")
        get.data
        return self.assertTrue()

if __name__ == '__main__':
    unittest.main()
