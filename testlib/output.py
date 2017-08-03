
from datetime import datetime
from xml.etree import ElementTree

def define_namespaces():
    ElementTree.register_namespace("ldr", "http://lib.uchicago.edu/ldr")
    ElementTree.register_namespace("dc", "http://purl.org/dc/elements/1.1/")
    ElementTree.register_namespace("dcterms", "http://purl.org/dc/terms/")
    ElementTree.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")

def build_envelope(outputname):
    root = ElementTree.Element(outputname)
    requestSent = ElementTree.SubElement(root, "{http://lib.uchicago.edu/ldr}requestReceivedTimeStamp")
    responseSent = ElementTree.SubElement(root, "{http://lib.uchicago.edu/ldr}responseSentTimeStamp")
    requestSent.text = datetime.now().isoformat()
    responseSent.text = datetime.now().isoformat()
    core = ElementTree.SubElement(root, "{http://lib.uchicago.edu/ldr}core")
    metadata = ElementTree.SubElement(core, "{http://lib.uchicago.edu/ldr}metadata")
    return root

def build_core(root):
    metadata = root.find("{http://lib.uchicago.edu/ldr}metadata")
    title = ElementTree.SubElement(metadata, '{http://purl.org/dc/elements/1.1/}title')
    title.text = "A Simple Title"
    date = ElementTree.SubElement(metadata, '{http://purl.org/dc/elements/1.1/}date')
    date.text = "1800"
    relation_one = ElementTree.SubElement(metadata, '{http://purl.org/dc/elements/1.1/}relation')
    relation_one.text = "testcollection"
    relation_one.set("http://www.w3.org/2001/XMLSchema-instancetype}type", "URL")
    relation_two = ElementTree.SubElement(metadata, '{http://purl.org/dc/elements/1.1/}relation')
    relation_two.set("http://www.w3.org/2001/XMLSchema-instancetype}type", "URL")
    relation_two.text = "secondtestcollection"
    identifier = ElementTree.SubElement(metadata, '{http://purl.org/dc/elements/1.1/}identifier')
    identifier.set("http://www.w3.org/2001/XMLSchema-instancetype}type", "URL")
    identifier.text = "https://dummyimage.com/200x300&text=test image!"
    return root

def add_an_extension(envelope, complex_element, name_string):
    extensions = envelope.find("{http://lib.uchicago.edu/ldr}extensions")
    if not extensions:
        extensions = ElementTree.SubElement(envelope, "{http://lib.uchicago.edu/ldr}extensions")
    extension = ElementTree.SubElement(extensions, "{http://lib.uchicago.edu/ldr}extension")
    name = ElementTree.SubElement(extension, "{http://lib.uchicago.edu/ldr}name")
    type = ElementTree.SubElement(extension, "{http://lib.uchicago.edu/ldr}type")
    type.text = "xml"
    name.text = name_string
    data = ElementTree.SubElement(extension, "{http://lib.uchicago.edu/ldr}data")
    ElementTree.SubElement(data, complex_element)
    return envelope

def create_simple__unit_xml_input(self):
    """creates a basic input XML record according to spec
    """
    define_namespaces()
    root  = build_envelope("ldr:input")
    root = build_core(root)
    return root

def create_complex_unit_xml_input(self):
    """creates an input XML record with 1 extension metdata according to spec
    """
    define_namespaces()
    root = build_envelope("{http://lib.uchicago.edu/ldr}input")
    root = build_core(root)
    root = add_an_extension(root, ElementTree.Element("{http://purl.org/dc/elements/1.1/}identifier"), "test")
    return root

def create_output_xml(self):
    """creates an output xml record according to spec
    """
    define_namespaces()
    root = build_envelope("{http://lib.uchicago.edu/ldr}output")
    return root