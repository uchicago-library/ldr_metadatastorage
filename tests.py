"""the module containing unit test code for the metadata storage api
"""

import os
import tempfile
import unittest

import metadatastorageapi
from testlib.output import *
from xml.etree import ElementTree

class TestToSpecOnePointO(unittest.TestCase):
    """the api test suite
    """
    def setUp(self):
        self.db_fd, metadatastorageapi.APP.config['DATABASE'] = tempfile.mkstemp()
        metadatastorageapi.APP.testing = True
        self.app = metadatastorageapi.APP.test_client()
        # with metadatastorageapi.APP.app_context():
        #     metadatastorageapi.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(metadatastorageapi.APP.config['DATABASE'])

    # Start of private methods

    def _convert_response_to_xml(self, response_data):
        try:
            return ElementTree.fromstring(response_data)
        except ElementTree.ParseError:
            return None

    def _universal_output_testing(self, resp):
        resp_root = ElementTree.parse(resp.data).getroot()
        req = resp_root.findall("{http://lib.uchicago.edu/ldr}request")
        response_sent_time = resp_root.findall("{http://lib.uchicago.edu/ldr}responseSentTimeStamp")
        request_received_time_stamp = resp_root.findall("{http://lib.uchicago.edu/ldr}requestReceivedTimeStamp")
        response_type = resp_root.findall("{http://lib.uchicago.edu/ldr}responseType")
        response = resp_root.findall("{http://lib.uchicago.edu/ldr}response")
        metadata = response[0].findall("{http://lib.uchicago.edu/ldr}metadata")
        check = self.assertEqual(req.count(), 1) & self.assertEqual(response_sent_time.count(), 1) &\
                self.assertEqual(request_received_time_stamp.count(), 1) & self.assertEqual(response_type.count(), 1) &\
                self.assertEqual(response.count(), 1) & self.assertEqual(metadata.count(), 1)
        return check

    # End of private methods

    # Start of posting data tests

    # def test_post_valid_non_asset_collection(self):
    #     define_namespaces()
    #     root = build_envelope("ldr:input")
    #     root = build_core(root)
    #     response = self.app.post("/collection/testOne")
    #     return self.assertEqual(response.status_code, 200)

    # def test_post_invalid_non_asset_collection(self):
    #     define_namespaces()
    #     root = build_envelope("ldr:input")
    #     root = build_core(root)
    #     response = self.app.post("/collection/testTwo")
    #     return self.assertEqual(response.status_code, 400)

    # def test_post_valid_asset_collection(self):
    #     define_namespaces()
    #     root = build_envelope("ldr:input")
    #     root = build_core(root)
    #     response = self.app.post("/collection/testThree")
    #     return self.assertEqual(response.status_code, 200)

    # def test_post_valid_asset_with_extension(self):
    #     define_namespaces()
    #     root = build_envelope("ldr:input")
    #     root = build_core(root)
    #     response = self.app.post("/collection/testFive")
    #     return self.assertEqual(response.status_code, 200)

    # def test_post_invalid_asset_with_extension(self):
    #     define_namespaces()
    #     root = build_envelope("ldr:input")
    #     root = build_core(root)
    #     response = self.app.post("/collection/testSix")
    #     return self.assertEqual(response.status_code, 400)

    # End of posting data tests

    # Start of aggregate endpoint tests

    def test_get_root_collections(self):
        response = self.app.get("/collections")
        response = self.app.get("/collection/testOne/core")
        if self._convert_response_to_xml(response.data):
            root = self._convert_response_to_xml(response.data)
            first_checks = self._universal_output_testing(root)
            relations = root.findall(
                "{http://lib.uchicago.edu/ldr}response/{http://lib.uchicago.edu/lib}metadata/{http://purl.org/dc/elements/1.1/}relation"
                )
            return self.assertTrue(first_checks) & self.assertGreaterEqual(relations.count(), 1)

    def test_get_collection_list(self):
        response = self.app.get("/collection/testOne/core")
        if self._convert_response_to_xml(response.data):
            root = self._convert_response_to_xml(response.data)
            first_checks = self._universal_output_testing(root)
            parts = root.findall(
                "{http://lib.uchicago.edu/ldr}response/{http://lib.uchicago.edu/lib}metadata/{http://purl.org/dc/elements/1.1/}hasPart"
                )
            return self.assertTrue(first_checks) & self.assertGreaterEqual(parts.count(), 1)

    def test_get_nested_collection_list(self):
        response = self.app.get("/collection/testOne/core")
        if self._convert_response_to_xml(response.data):
            root = self._convert_response_to_xml(response.data)
            first_checks = self._universal_output_testing(root)
            isPartOf = root.findall(
                "{http://lib.uchicago.edu/ldr}response/{http://lib.uchicago.edu/lib}metadata/{http://purl.org/dc/elements/1.1/}isPartOf"
                )
            return self.assertTrue(first_checks) & self.assertGreaterEqual(isPartOf.count(), 1)
        else:
            return self.assertTrue(False)

    def test_get_extension_list(self):
        response = self.app.get("/collection/testOne/core")
        if self._convert_response_to_xml(response.data):
            root = self._convert_response_to_xml(response.data)
            first_checks = self._universal_output_testing(root)
            relations = root.findall(
                "{http://lib.uchicago.edu/ldr}response/{http://lib.uchicago.edu/lib}metadata/{http://purl.org/dc/elements/1.1/}relation"
                )
            return self.assertTrue(First_checks) & self.assertGreaterEqual(relations.count(), 1)
        else:
            return self.assertTrue(False)

    # End of aggregate endpoint tests

    # Start of atomic endpoint tests

    def test_get_core_metadata(self):
        response = self.app.get("/collection/testOne/core")
        if self._convert_response_to_xml(response.data):
            root = self._convert_response_to_xml(response.data)
            first_checks = self._universal_output_testing(root)
            title = True if root.findall(
                "{http://lib.uchicago.edu/ldr}response/{http://lib.uchicago.edu/ldr}metadata/{http://purl.org/dc/elements/1.1/}title"
                ).count() == 1 else False
            identifier = True if root.findall(
                "{http://lib.uchicago.edu/ldr}response/{http://lib.uchicago.edu/ldr}metadata/{http://purl.org/dc/elements/1.1/}date"
                ).count() == 1 else False
            return self.assertTrue(first_checks) & self.assertTrue(title) & self.assertTrue(identifier)
        else:
            return self.assertTrue(False)

    def test_get_an_extension(self):
        response = self.app.post("/collection/testFive/extensions/structuralMetadata")
        if self._convert_response_to_xml(response.data):
            root = self._convert_response_to_xml(response.data)
            first_checks = self._universal_output_testing(root)
            extension = root.findall("{http://lib.uchicago.edu/ldr}response/{http://lib.uchicago.edu/ldr}extension")
            ext_type = extension.find("{http://lib.uchicago.edu/ldr}type")
            ext_type_valid = True if ext_type.text in ['text','json','xml'] else False
            ext_name = True if extension.find("{http://lib.uchicago.edu/ldr}name") else False
            data = True if extension.find("{http://lib.uchicago.edu/ldr}data") else False
            return first_checks & self.assertTrue(ext_type_valid) & self.assertTrue(ext_name) & self.assertTrue(data)
        else:
            return self.assertTrue(False)

    # End of atomic endpoint tests

    # Start of contextual endpoint tests

    def test_root_endpoint_context(self):
        response = self.app.get("/")
        if self._convert_response_to_xml(response.data):
            root = self._convert_response_to_xml(response.data)
            first_checks = self._universal_output_testing(root)
            relations = root.findall(
                "{http://lib.uchicago.edu/ldr}response/{http://lib.uchicago.edu/lib}metadata/{http://purl.org/dc/elements/1.1/}relation"
                )
            return first_checks & self.assertGreaterEqual(relations.count(), 1)
        else:
            return self.assertTrue(False)

    def test_a_collection_context(self):
        response = self.app.get("/")
        if self._convert_response_to_xml(response.data):
            root = self._convert_response_to_xml(response.data)
            first_checks = self._universal_output_testing(root)
            relations = root.findall(
                "{http://lib.uchicago.edu/ldr}response/{http://lib.uchicago.edu/lib}metadata/{http://purl.org/dc/elements/1.1/}relation"
                )
            return first_checks & self.assertGreaterEqual(relations.count(), 1)
        else:
            return self.assertTrue(False)

    # End of contextual endpoint tests

if __name__ == '__main__':
    unittest.main()
