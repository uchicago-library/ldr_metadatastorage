# README

## Glossary of terms

- intellectual unit is a set of assets that comprise a complete work (whether a piece of art, a photograph, a book, or some other output) created by an individual or group of individuals
- (metadata) resource is a representation of description about an intellectual unit
- endpoint is a particular context available to a (metadata) resource that will provide some functionality
- functionality is either a.) the answer to a particular question about a particular resource or b.) some action or set of actions that transforms the resource identified into something new for the client to consume
- field is a particular piece of metadata. ex. title is a field
- core (metadata) is the REQUIRED descriptive fields: a.) 1 title field, b.) 1 creator field, c.) 1 date field, d.) 1 or more identifier identifier fields, e.) 1 or more relation fields
- extension (metadata) is an OPTIONAL descriptive metadata resource that is subordinate to the core (metadata)

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

This means that in order to provide functionality for the the ldr metadata storage must be able to retriever assets from either asset storage or any arbitrary outside storage accessible on the web.

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

COROLLARY: the metadata storage should be able to store technical metadata about assets in digital collections. This technical metadata is currently being stored in asset storage, but there is a strong argument to be made that doing this "muddies the water" between asset and metadata. Asset ought to be strictly defined as a byte stream representing an intellectual unit or some portion of an intellectual unit. By storing technical metadata, which by definition is not a byte stream representing a whole or some port of an intellectual unit but rather information about the bytestream the asset storage is being forced to perform a task that is a violation of its primary function.

## interfaces for ldr metadata storage to provide for depositing clients

### /submission

communication protocol: Web
communication method: Post

#### valid input

There are three types of valid input. The first is for input from a remote source. The second one is for input from the library which means that assets are in asset storage. The third is for input that includes non-core metadata.

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

## interfaces for ldr metadata storage to provide for requesting clients

### /[identifier]

This endpoint MUST return all available contexts for the resource identified. All resources have the following contexts:

- core
- extensions

communication protocol: Web
communication method: GET

```xml
<?xml version="1.0" encoding="utf-8"?>
<metadata_store_output>
    <request>/[identifier]</request>
    <response>
        <available_requests>
            <available_request>/[identifier]/core</avaiable_request>
            <available_request>/[identifier]/extensions</avaiable_request>
        </available_requests>
    </response>
</metadata_store_output>
```

### /[identifier]/core

This endpoint must return the core metadata for the resource identified. This is required in order to provide cross-collection browsing functionality to frontend interfaces.

communication protocol: Web
communication method: GET

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
            <dc:identifier xsi:type="dcterms:URI">/mvol-0001-0002-0004</dc:identifier>
            <dc:relation>campub</dc:relation>
            <dc:relation>ldr</dc:relation>
        </metadata>
    </response>
</metadata_store_output>
```

### /[identifier]/extensions

This endpoint MUST return a list of all extensions available for a particular resource. The ldr metadata storage system DOES NOT makes any guarantee about providing contexts for extension metadata since there is no theoretical limit on the diversity of extension metadata schemes that might be available for a particular resource. The ldr metadata storage only guarantees that it will store all extensions that are added to the system and provide the ability for clients interfaces to retrieve them. The client interfaces MUST have the business logic to know what to do with the extension metadata.

communication protocol: Web
communication method: GET

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

### /[identifier]/extensions/[extension metadata]

communication protocol: Web
communication method: GET

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