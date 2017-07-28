# README

## Glossary of terms

- intellectual unit is a set of assets that comprise a complete work (whether a piece of art, a photograph, a book, or some other output) created by an individual or group of individuals
- unit is an abbreviation of intellectual unit
- asset is a byte stream representing an intellectual unit whether in-whole or in-part
- (metadata) resource is a representation of description about an intellectual unit
- endpoint is a particular context available to a (metadata) resource that will provide some functionality
- functionality is either a.) the answer to a particular question about a particular resource or b.) some action or set of actions that transforms the resource identified into something new for the client to consume
- field is a particular piece of metadata. ex. title is a field
- core (metadata) is the REQUIRED descriptive fields: a.) 1 title field, b.) 1 creator field, c.) 1 date field, d.) 1 or more identifier identifier fields, e.) 1 or more relation fields
- extension (metadata) is an OPTIONAL descriptive metadata resource for an intellectual unit
- client is a a program running on a server that is requesting a resource. This client may be acting on behalf of a biological being.

## Shortcuts

- [new collection post specification](####Specification-for-posting-a-new-collection)
- [new unit post specification](####Specification-for-posting-a-new-unit)

## Requirements for the metadata storage system

Metadata storage must be able to answer the following questions about an intellectual unit

1. What is the collection that this unit belongs to use as the main access point for the user
1. what is the title of this unit to display as the second access point for the user
1. what is the publication date of this unit to use as third acess point for the user
1. Who is the creator of this unit to use as the fourth access point for the user 5. What is the identifier for this resource to be able to locate the assets associated with this unit in order to display them to the user
1. What is the identifier of the asset whether library-controlled or remote so that the ldr metadata storage can point the user to the asset or assets that are part of this unit

There are two types of metadata that will be in the ldr metadata storage system.

1. units that belong to the University of Chicago library and which all assets associated are in asset storage
1. units that do not belong to the University of Chicago library and which assets are stored elsewhere

This means that in order to provide a REQUIRED functionality, ldr metadata storage must be able to retrieve assets from either asset storage or any arbitrary outside storage accessible. It is therefore MANDATORY that all assets be available over the public Web.

This also means the ldr metadata storage must be able to distinguish between a remote asset and a library-controlled asset.

In order to distinguish between the two types of assets, there must be some marker for the ldr metadata storage to use to make this distinction. One marker will lead the ldr metadata storage to locate the assets from the digcoll retriever. The other will tell it to check if the address is valid. If the address is not valid, the ldr metadata storage should notify the administrators of the ldr metadata storage as well as the person attempting to ingest material into the ldr metadata storage.

The asset storage identifier should be a URI, because the ldr metadata storage must know from what host to pull the assets and we must assume that this host will change over time.

The remote storage identifier must be a valid URL to the location of the asset on the web.

We have to assume that there will be a variety of descriptive metadata formats used. Since there are five known metadata formats currently being used in library digital collections.

- TEI
- EAD
- MODS
- VRACore
- OCR

This means that the metadata storage must be able to store a variety of metadata formats that are not actionable by the metadata storage. The metadata storage must have a single schema that it can interpret in order to provide the five functions defined at the beginning of this document.

COROLLARY: the metadata storage should be able to store technical metadata about assets in digital collections. This technical metadata is currently being stored in asset storage, but there is a strong argument to be made that doing this "muddies the water" between asset and metadata. Asset ought to be strictly defined as a byte stream representing an intellectual unit or some portion of an intellectual unit. By storing technical metadata, which by definition is not a byte stream representing a whole or some port of an intellectual unit but rather information about the byte stream the asset storage is being forced to perform a task that is a violation of its primary function.

## interfaces for ldr metadata storage

### /

communication protocol: Web

communication method: GET

```xml
<?xml version="1.0" encoding="utf-8"?>
<metadata_store_output>
    <request>/</request>
    <response>
        <available_contexts>
            <available_contexts>/collections</available_contexts>
            <available_contexts>/units</available_contexts>
        </available_contexts>
    </response>
</metadata_store_output>
```

### /collections

communication protocols: Web

communication methods: GET, POST

The ldr metadata storage offers a GET method on the collections endpoint in order to retrieve a list of all collections in the metadata storage. The ldr metadata storage guarantees that a GET request from this endpoint will give the consuming client an up-to-date list of collections available in the ldr metadata storage.

```xml
<?xml version="1.0" encoding="utf-8"?>
<metadata_store_output>
    <request>/collections</request>
    <response>
        <available_collections>
            <available_collection>/collections/[collection one identifier]</available_collection>
            <available_collection>/collections/[collection two identifier]</available_collection>
        </available_collections>
    </response>
</metadata_store_output>
```

#### Specification for posting a new collection

The ldr metadata storage also offers a POST method on the collections endpoint in order to allow clients to add new collections to the metadata storage. The ldr metadata storage guarantees that a POST request from this endpoint will add the inputted collection to the ldr metadata storage so long as the input obeys the following rules

- collection name is unique to the ldr metadata storage
- post data obeys the defined specification
    1. POST data is well-formed XML in UTF-8 encoding
    1. the root element of the XML document is "metadata_store_input" with no namespace
    1. the second element in the XML document beneath the root is "core" with no namespace. There can be only one instance of this element.
    1. The third element in the XML document is metadata with an implicit namespace of http://example.org/myapp. There can be only one instance of this element.
    1. The metadata element has the follow explicit namespaces xmlns:dc="http://purl.org/dc/elements/1.1/", xmlns:dcterms="http://purl.org/dc/terms/" and xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance".
    1. The metadata element is a compound element that contains the following
        - the first instance of an element dc:title that contains a string containing multiple words. This is the formal title of the collection.
        - the second instance  an element dc:title that contains a single word. This is the unique identifier for the collection.
        - one instance of an element dc:description that contains multiple complete sentences. However, it is advised that you keep number of sentences to at most 4 unless there is a compelling need. This is the description of the collection, particulary focusing on how this collection is significant to the library.

This is an example to use for a complete understanding. Do not copy this example, since it is strictly a sample exercise and should not be considered canonical data.

```xml
<?xml version="1.0" encoding="utf-8"?>
<metadata_store_input>
    <core>
        <metadata
        xmlns="http://example.org/myapp/"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:dcterms="http://purl.org/dc/terms/">
            <dc:title>[a long form and formal title of the collection e.g. Richard G. Maynard Papers. Digital Collection]</dc:title>
            <dc:title>[a short form one-word title of the collection that can be used as the identifier for the collection e.g. maynard]</dc:title>
            <dc:description>[1-4 sentences describing how this collection is significant to the library]</dc:description>
        </metadata>
    </core>
</metadata_store_input>
```

### /collections/[collection identifier]

communication protocols: Web

communication methods: GET

```xml
<?xml version="1.0" encoding="utf-8"?>
<metadata_store_output>
    <request>/collections[collection identifier]</request>
    <response>
        <available_intellectual_units>
            <available_intellectual_unit>/unit/[intellectual unit identifier one]/</available_intellectual_unit>
            <available_intellectual_unit>/unit/[intellectual unit identifer two]</available_intellectual_unit>
        </available_intellectual_units>
    </response>
</metadata_store_output>
```

### /units

communication protocol: Web

communication methods: GET, POST

The ldr metadata storage offers a GET method on the units endpoint in order to retrieve a list of the intellectual units in the system. The ldr metadata storage guarantees that a request to this endpoint will provide an up-to-date list of all intellectual units in the system.

```xml
<?xml version="1.0" encoding="utf-8"?>
<metadata_store_output>
    <request>/collections[collection identifier]</request>
    <response>
        <available_intellectual_units>
            <available_intellectual_unit>/unit/[intellectual unit identifier one]/</available_intellectual_unit>
            <available_intellectual_unit>/unit/[intellectual unit identifer two]</available_intellectual_unit>
        </available_intellectual_units>
    </response>
</metadata_store_output>
```

#### Specification for posting a new unit

The ldr metadata storage also offers a POST method on the units endpoint in order to add a new intellectual unit to the system. The ldr metadata storage guarantees that a POST request to this endpoint will add the inputted intellectual unit to the system as long as the input obeys the following rules

- the intellectual unit is unique to the ldr metadata storage system
- the input obeys the defined specification

```xml
<?xml version="1.0" encoding="utf-8"?>
<metadata_store_input>
    <core>
        <metadata
        xmlns="http://example.org/myapp/"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://example.org/myapp/ http://example.org/myapp/schema.xsd"
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:dcterms="http://purl.org/dc/terms/">
            <dc:title>This is a title</dc:title>
            <dc:creator>John Doe</dc:title>
            <dc:date>1980-02-16</dc:date>
            <dc:identifier xsi:type="dcterms:URL">http://wwww.example.com/book1.pdf</dc:identifer>
            <dc:relation>campub</dc:relation>
            <dc:relation>ldr</dc:relation>
        </metadata>
    </core>
</metadata_store_input>
```

```xml
<?xml version="1.0" encoding="utf-8"?>
<metadata_store_input>
    <core>
        <metadata
        xmlns="http://example.org/myapp/"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://example.org/myapp/ http://example.org/myapp/schema.xsd"
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:dcterms="http://purl.org/dc/terms/">
            <dc:title>This is a title</dc:title>
            <dc:creator>John Doe</dc:title>
            <dc:date>1980-02-16</dc:date>
            <dc:identifier xsi:type="dcterms:URI">/mvol-0001-0002-0004</dc:identifier>
            <dc:relation>campub</dc:relation>
            <dc:relation>ldr</dc:relation>
        </metadata>
    </core>
</metadata_store_input>
```

```xml
<?xml version="1.0" encoding="utf-8"?>
<metadata_store_input>
    <core>
        <metadata
        xmlns="http://example.org/myapp/"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://example.org/myapp/ http://example.org/myapp/schema.xsd"
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:dcterms="http://purl.org/dc/terms/">
            <dc:title>This is a title</dc:title>
            <dc:creator>John Doe</dc:title>
            <dc:date>1980-02-16</dc:date>
            <dc:identifier xsi:type="dcterms:URI">/mvol-0001-0002-0004</dc:identifier>
            <dc:relation>campub</dc:relation>
            <dc:relation>ldr</dc:relation>
        </metadata>
    </core>
    <extensions>
        <extension>
            <!-- insert first optional extension metadata record here -->
        </extension>
        <extension>
            <!-- insert second optional extension metadata record here -->
        </extension>
    </extensions>
</metadata_store_input>
```

### /units/[intellectual unit identifier]

communication protocol: Web

communication methods: GET

This endpoint MUST return all available contexts for the intellectual unit identified. All intellectual units have the following contexts.

- core (MANDATORY)
- extensions (OPTIONAL)

```xml
<?xml version="1.0" encoding="utf-8"?>
<metadata_store_output>
    <request>/[identifier]</request>
    <response>
        <available_contexts>
            <available_context>/[identifier]/core</avaiable_context>
            <available_context>/[identifier]/extensions</avaiable_context>
        </available_contexts>
    </response>
</metadata_store_output>
```

### /units/[intellectual unit identifier]/core

communication protocol: Web

communication methods: GET

error conditions: no core (metadata) resource available

This endpoint must return the core (metadata) resource for the intellectual unit identified. This is required in order to provide cross-collection browsing functionality of all intellectual units in the ldr metadata storage to frontend interfaces. The core (metadata) MUST include an identifier of type dcterms:URL for every asset for this intellectual unit. The ldr metadata storage MAY include an identifier of type dcterms:URI if this intellectual unit is part of a library digital collection. If there is an  identifier of type dcterms:URI, then the consuming client MUST be able to retrieve the project-specific explanation of the relationships between assets for the intellectual unit identified. If there is no identifier of type dcterms:URI than the consuming client MUST contain the business logic for defining the relationships between the assets itself.

```xml
<?xml version="1.0" encoding="utf-8"?>
<metadata_store_output>
    <request>/[identifier]/core</request>

    <response>
        <metadata
        xmlns="http://example.org/myapp/"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://example.org/myapp/ http://example.org/myapp/schema.xsd"
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:dcterms="http://purl.org/dc/terms/">
            <dc:title>This is a title</dc:title>
            <dc:creator>John Doe</dc:title>
            <dc:date>1980-02-16</dc:date>
            <dc:identifier xsi:type="dcterms:URI">/[intellectual unit identifier]</dc:identifier>
            <dc:identifier xsi:type="dcterms:URL">[http scheme]://[asset storage host]/[asset identifier]</dc:identifier>
            <dc:relation type="dcterms:URL">/[http scheme]://[ldr metadata storage host]/collections/[collection identifier]</dc:relation>
            <dc:relation type="dcterms:URL">[http scheme]://[ldr metadata storage host]/collections/ldr</dc:relation>
        </metadata>
    </response>
</metadata_store_output>
```

### /units/[intellectual unit identifier]/extensions

communication protocol: Web

communication methods: GET

error conditions: no extensions available

This endpoint MUST return a list of all extensions available for a particular intellectual unit. The ldr metadata storage system DOES NOT makes any guarantee about providing contexts for extension metadata since there is no theoretical limit on the diversity of extension metadata schemes that might be available for a particular resource. The ldr metadata storage only guarantees that it will store all extensions that are added to the system and provide the ability for clients interfaces to retrieve them. The client interfaces MUST have the business logic to know what to do with the extension metadata.

```xml
<?xml version="1.0" encoding="utf-8"?>
<metadata_store_output>
    <request>/[identifier]/extensions</request>
    <response>
        <extension>/[identifier]/extensions/vracore</extension>
        <extension>/[identifier]/extensions/mods</extension>
        <extension>/[identifier]/extensions/ocr</extension>
    </response>
</metadata_store_output>
```

### /units/[intellectual unit identifier]/extensions/[extension metadata]

communication protocol: Web

communication methods: GET

error conditions: extension requested does not exist

This endpoint MUST return the extension that is specified for the intellectual unit identified.

```xml
<?xml version="1.0" encoding="utf-8"?>
<metadata_store_output>
    <request>/[identifier]/extensions/vracore</request>
    <response>
        <extension>
            <!-- VRACore metadata here -->
        </extension>
    </response>
</metadata_store_output>
```