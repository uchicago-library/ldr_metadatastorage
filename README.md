# Introduction

This is a specification for how to get input into the metadata storage and how to get output from the metadata storage. As such, it will define a specification for how to add metadata to the metadata storage and the interface endpoints that the metadata storage will make available in order to receive input. It will also define the  endpoints that the metadata storage must make available to allow clients to access the metadata from the metadata storage, and the format that the output body will take.

# Options for master metadata record

```

<?xml version="1.0"?>
<metadata
  xmlns="http://example.org/myapp/"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://example.org/myapp/ http://example.org/myapp/schema.xsd"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:dcterms="http://purl.org/dc/terms/">
    <dc:title>This is a title</dc:title>
    <dc:creator>John Doe</dc:title>
    <dc:date>1980-02-16</dc:date>
    <dc:identifier xsi:type="dcterms:URI">/mvol-00001-0002-00001/stat</dc:identifier>
    <dc:identifier xsi:type="dcterms:URL">http://wwww.example.com/book1.pdf</dc:identifer>
    <dc:relation>campub</dc:relation>
    <dc:relation>ldr</dc:relation>
</metadata>

```

```

<metadata_wrapper>
    <core_metadata>
        <metadata
              xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
              xmlns:dc="http://purl.org/dc/elements/1.1/"
              xmlns:dcterms="http://purl.org/dc/terms/">
            <dc:title>This is a title</dc:title>
            <dc:creator>John Doe</dc:title>
            <dc:date>1980-02-16</dc:date>
            <dc:identifier xsi:type="dcterms:URI">/mvol-00001-0002-00001/stat</dc:identifier>
            <dc:identifier xsi:type="dcterms:URL">http://wwww.example.com/book1.pdf</dc:identifer>
            <dc:relation>campub</dc:relation>
            <dc:relation>ldr</dc:relation>
        </metadata>
    </core_metadata>
    <optional_metadata metadata_namespace="http://www.vraweb.org/vracore4.htm">
        <!-- vra core metadata inserted here -->
    </optional_metadata>
    <optional_metadata metadata_namespace="http://www.loc.gov/mods/v3">
        <!-- mods metadata inserted here -->
    </optional_metadata>
    <structural_metadata>
        <text>
            <!-- insert structural metadata from .struct.txt here -->
        </text>
    </structural_metadata>
    <structural_metadata>
        <xml>
            <!-- insert xml structural metadata here -->
        </xml>
    </structural_metadata>
</metadata_wrapper>

{'core': {
    'title': 
    'date':
    'creator':
    'asset_identifier': '/mvol/0001/0002/0003/nav',
    'external_identifier': {
        'type': 'book',
        'parts': [
            {'type':'composite',
             'asssets': [
                 {'type':'url',
                  'source': 'http://example.com/foo/page1.tif'},
                {'type': 'uri',
                 'source': '/mvol-0001-0002-0003_0001'}
             ]
            }
    }
}
}
```

The metadata storage will do the following on reception of the data

1. extract the core data and generate a dublin core record conforming to dublin core schema for adding to cross-browsing metadata storage

2. read though extensions list and check that the extension type is valid.

# Master Metadata Container

```

<metadata>
    <core>
        <title></title>
        <date></date>
        <dentifier></identifier>
        <identifier></identiifer>
        <relation>
    </core>
</metadata>

```

Metadata storage must be able to answer the following questions about an intellectual unit

1. What is the collection that this unit belongs to use as the main access point for the user
2. what is the title of this unit to display as the second access point for the user
3. what is the publication date of this unit to use as third acess point for the user
4. Who is the creator of this unit to use as the fourth access point for the user
5. What is the identifier for this resource to be able to locate the assets associated with this unit in order to display them to the user

There are two types of metadata that will be in the ldr metadata storage system.

1. units that belong to the University of Chicago library and which all assets associated are in asset storage
2. units that do not belong to the University of Chicago lbrary and which assets are stored elsewhere

This means that in order to provide functionality for the the ldr metadata storage must be able to retriever assets from either asset storage or any arbitrary outside storage accessible on the web.

This also means the ldr metadata storage must be able to distinguish between a remote asset and a library-controlled asset.