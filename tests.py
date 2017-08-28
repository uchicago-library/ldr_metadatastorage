"""the module containing unit test code for the metadata storage api
"""

from base64 import b64decode
import os
import tempfile
import unittest
from xml.etree import ElementTree
from sys import stderr
from testlib.output import build_core, build_envelope, define_namespaces
import metadatastorageapi

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

    def _test_for_right_num(self, find_els, right_num):
        if find_els:
            return len(find_els) == right_num

    def _comp_for_truthy(self, a_list):
        out = True
        for n in a_list:
            out &= n
        return out

    def _universal_output_testing(self, resp):
        resp_root = resp
        req = resp_root.findall("{http://lib.uchicago.edu/ldr}request")
        s_time = resp_root.findall("{http://lib.uchicago.edu/ldr}responseSentTimeStamp")
        r_time = resp_root.findall("{http://lib.uchicago.edu/ldr}requestReceivedTimeStamp")
        r_type = resp_root.findall("{http://lib.uchicago.edu/ldr}responseType")
        resp = resp_root.findall("{http://lib.uchicago.edu/ldr}response")
        mdata = resp[0].findall("{http://lib.uchicago.edu/ldr}metadata")
        out = self._comp_for_truthy([self._test_for_right_num(x, 1)
                                     for x in [req, s_time, r_time, r_type, mdata]])
        return out

    def _opening_check(self, resp):
        if resp.get_data():
            data = self._convert_response_to_xml(resp.get_data())
            first_checks = self._universal_output_testing(data)
            return (first_checks, data)
        else:
            return (False, None)

    # End of private methods

    # Start of posting data tests

    # Start of aggregate endpoint tests

    def test_get_root_collections(self):
        """test endpoint /collections/[collection identifier]

        should return output that looks like:

        <output>
            <request/>
            <requestReceivedTimeStamp/>
            <responseSentTimeStamp/>
            <responseType/>
            <response>
                <metadata>
                    <dc:relation xsi:type="dcterms:URI"/>
                    <dc:relation xsi:type="dcterms:URI"/>
                    <dc:relation xsi:type="dcterms:URI"/>
                </metadata>
            </response>
        </output>

        """
        response = self.app.get("/")
        answer = self._opening_check(response)
        if answer[1]:
            root = answer[1]
            rels = [x.tag for x in root.find(
                "{http://lib.uchicago.edu/ldr}response" +
                "/{http://lib.uchicago.edu/ldr}metadata"
            )]
            check = answer[0]
            rels = ([x for x in rels if x == "{http://purl.org/dc/elements/1.1/}relation"])
            check &= len(rels) == 1
        else:
            # this means th]at the response didn't get picked up for some reason
            stderr.write("cannot open response for /.\n")
            return self.assertTrue(check)
        return self.assertTrue(check)

    def test_get_root_list_collections(self):
        """test endpoint /collections/[collection identifier]

        should return output that looks like:

        <output>
            <request/>
            <requestReceivedTimeStamp/>
            <responseSentTimeStamp/>
            <responseType/>
            <response>
                <metadata>
                    <dc:relation xsi:type="dcterms:URI"/>
                    <dc:relation xsi:type="dcterms:URI"/>
                    <dc:relation xsi:type="dcterms:URI"/>
                </metadata>
            </response>
        </output>
        """
        response = self.app.get("/collections")
        answer = self._opening_check(response)
        if answer[1]:
            root = answer[1]
            parts = root.find(
                "{http://lib.uchicago.edu/ldr}response/" +
                "{http://lib.uchicago.edu/ldr}metadata"
            )
            parts = [x for x in parts if x.tag == "{http://purl.org/dc/elements/1.1/}hasPart"]
            check = answer[0]
            print(parts)
            check &= len(parts) >= 1
            print(check)
        else:
            check = answer[0]
        return self.assertTrue(check)

    def test_get_nested_collection_list(self):
        """test endpoint /collections/[collection identifier]/[sub-collection identifier]

        should return output that looks like:

        <output>
            <request/>
            <requestReceivedTimeStamp/>
            <responseSentTimeStamp/>
            <responseType/>
            <response>
                <metadata>
                    <dc:relation xsi:type="dcterms:URI"/>
                    <dc:relation xsi:type="dcterms:URI"/>
                    <dc:relation xsi:type="dcterms:URI"/>
                </metadata>
            </response>
        </output>
        """
        response = self.app.get("/collections/collection2")
        answer = self._opening_check(response)
        if answer[1]:
            root = answer[1]
            parts = root.find(
                    "{http://lib.uchicago.edu/ldr}response/" +
                    "{http://lib.uchicago.edu/ldr}metadata"
            )
            print(parts)
            parts = [x for x in parts if x.tag == "{http://purl.org/dc/elements/1.1/}hasPart"]
            print(parts)
            check = answer[0]
            check &= len(parts) >= 1
            print(check)
        else:
            check = answer[0]
        return self.assertTrue(check)

    def test_get_double_nested_collection_list(self):
        """test endpoint /collections/[collection identifier]/[sub-collection identifier]

        should return output that looks like:

        <output>
            <request/>
            <requestReceivedTimeStamp/>
            <responseSentTimeStamp/>
            <responseType/>
            <response>
                <metadata>
                    <dc:relation xsi:type="dcterms:URI"/>
                    <dc:relation xsi:type="dcterms:URI"/>
                    <dc:relation xsi:type="dcterms:URI"/>
                </metadata>
            </response>
        </output>
        """
        response = self.app.get("/collections/collection2-subcollection1")
        answer = self._opening_check(response)
        if answer[1]:
            root = answer[1]
            parts = root.find(
                    "{http://lib.uchicago.edu/ldr}response/" +
                    "{http://lib.uchicago.edu/ldr}metadata"
            )
            print(parts)
            print(ElementTree.tostring(root))
            parts = [x for x in parts]
            print(parts)
            check = answer[0]
            check &= len(parts) >= 1
            print(check)
        else:
            check = answer[0]
        return self.assertTrue(check)

    def test_get_core_metadata(self):
        """test endpoint /collection/[collection identifier]/core

        should return output that looks like:

        <output>
            <request/>
            <requestReceivedTimeStamp/>
            <responseSentTimeStamp/>
            <responseType/>
            <response>
                <metadata>
                    <dc:title/>
                    <dc:identifier/>
                    <dc:creator/>
                    <dc:date/>
                    <dc:description/>
                    <dc:isPartOf/>
                    <dc:hasPartOf/>
                </metadata>
            </response>
        </output>
        """
        response = self.app.get("/collection/collection2-subcollection1/core")
        answer = self._opening_check(response)
        if answer[1]:
            root = answer[1]
            metadata = root.find(
                        "{http://lib.uchicago.edu/ldr}response/" +
                        "{http://lib.uchicago.edu/ldr}metadata"
            )
            identifier = [x for x in metadata if x.tag == "{http://purl.org/dc/elements/1.1/}identifier"]
            title =  [x for x in metadata if x.tag == "{http://purl.org/dc/elements/1.1/}title"]
            check = answer[0]
            check &= len(identifier) >= 1
            check &= len(title) >= 1
        else:
            check = answer[1]
        return self.assertTrue(check)
        #     identifier = True if root.findall(
        #         "{http://lib.uchicago.edu/ldr}response/{http://lib.uchicago.edu/ldr}metadata/{http://purl.org/dc/elements/1.1/}date"
        #         ).count() == 1 else False
        #     return self.assertTrue(first_checks) & self.assertTrue(title) & self.assertTrue(identifier)
        # else:
        #     return self.assertTrue(False)

    def test_get_extension_list(self):
        """test endpoint /collection/[collection identifier]/extensions

        should return output that looks like:

        <output>
            <request/>
            <requestReceivedTimeStamp/>
            <responseSentTimeStamp/>
            <responseType/>
            <response>
                <metadata>
                    <dc:relation xsi:type="dcterms:URI"/>
                    <dc:relation xsi:type="dcterms:URI"/>
                    <dc:relation xsi:type="dcterms:URI"/>
                </metadata>
            </response>
        </output>
        """
        response = self.app.get("/collection/collection2-subcollection1-item1/proxies")
        answer = self._opening_check(response)
        if answer[1]:
            root = answer[1]
            metadata = root.find(
                        "{http://lib.uchicago.edu/ldr}response/" +
                        "{http://lib.uchicago.edu/ldr}metadata"
            )
            rels = [x for x in metadata if x.tag == "{http://purl.org/dc/elements/1.1/}relation"]
            check = answer[0]
            check &= len(rels) >= 1
        else:
            check = answer[0]
        return self.assertTrue(check)

    def test_get_an_extension(self):
        response = self.app.get("/collection/collection2-subcollection1-item1/proxies/collection2-subcollection1-item1-mods")
        if response.status_code:
            data = response.get_data()
            check = True
            try:
                b64decode(data)
                check &= True
            except ValueError:
                check &= False
        else:
            check = False
        return self.assertTrue(check)

if __name__ == '__main__':
    unittest.main()
