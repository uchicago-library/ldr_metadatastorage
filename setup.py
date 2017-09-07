"""an api designed for use by the UChicago LDR to send and receive metadata.

Current implementation goal: store XML in Marklogic and have this API send/receive,
validate POST data, validate GET requests

The API should be storage backend agnostic like the asset storage API so that the
library can switch backend when it needs to.
"""

from setuptools import setup

def readme():
    output = ""
    try:
        with open("README.md", "r") as read_file:
            output = read_file.read()
    except IOError:
        output = "An API for use by the UChicago library to facilitate metadata storage."
    return output

setup(
    name='metadatastorageapi',
    version='0.9.1',
    author = ['Tyler Danstrom', 'Brian Balsamo'],
    author_email = ['tdanstrom@uchicago.edu', 'balsamo@uchicago.edu'],
    description=readme(),
    license = "LGPL3.0",
    long_description=readme(),
    packages=['metadatastorageapi', 'testlib'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['flask', 'flask_env', 'flask_restful', 'pytest'],
)

