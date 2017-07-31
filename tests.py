import unittest
import json
from os import environ, getcwd
from os.path import join
from urllib.parse import quote

import metadatastorageapi


class MetadataStorageTest1(unittest.TestCase):

    def setUp(self):
        self.app = metadatastorageapi.APP.test_client()
        metadatastorageapi.blueprint.BLUEPRINT.config = {
            "MVOL_OWNCLOUD_ROOT": join(getcwd(), "sandbox", "mock_oc_root"),
            "MVOL_OWNCLOUD_USER": "ldr_oc_admin",
            "MVOL_OWNCLOUD_SUBPATH": "Preservation Unit"
        }

    def tearDown(self):
        pass

    def testTwoAndTwo(self):
        return 2 + 2 == 4

if __name__ == '__main__':
    unittest.main()