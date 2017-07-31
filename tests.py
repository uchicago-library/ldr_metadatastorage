import unittest
import json
from os import environ, getcwd
from os.path import join
from urllib.parse import quote

import metadatastorageapi


class TestingUnitTest(unittest.TestCase):

    def test_TwoAndTwo(self):
        self.assertEqual(2+2, 4) 

    def test_AString(self):
        self.assertIsInstance("foo", str)

if __name__ == '__main__':
    unittest.main()
