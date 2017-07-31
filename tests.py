import unittest
import json
from os import environ, getcwd
from os.path import join
from urllib.parse import quote

import metadatastorageapi


class TestingUnitTest(unittest.TestCase):

    def setupUp(self):
        self.app = metadatastorageapi.APP.test_client()

    def tearDown(self):
        pass

    def _response_200(self, rv):
        self.assertEqual(rv.status_code, 200)

    def test_rootURL(self):
        get = self.app.get("/")
        return self._response_200(get)

    def test_CollectionsURL(self):
        get = self.app.get("/units")
        return self._response_200(get)

    def test_zeroDepthCollectionURL(self):
        get = self.app.get("/units/{}/".format("foo"))
        return self._response_200(get)

    def test_nestedCollectionURL(self):
        get = self.app.get("/units/{}/{}/".format("foo", "bar"))
        return self._response_200(get)

    def test_coreURL(self):
        get = self.app.get("/units/{}/core".format("foo"))
        return self._response_200(get)

    def test_extensionsURL(self):
        get = self.app.get("/units/{}/extensions/".format("foo"))
        return self._response_200(get)

    def test_anExtensionsURL(self):
        get = self.app.get("/units/{}/extensions/{}/".format("foo", "bar"))


if __name__ == '__main__':
    unittest.main()
