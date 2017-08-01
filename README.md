[![Build Status](https://travis-ci.org/uchicago-library/ldr_metadatastorage.svg?branch=master)](https://travis-ci.org/uchicago-library/ldr_metadatastorage)

# README

## Introduction

Metadata storage must be able to answer the following questions about an intellectual unit.

1. What collection(s) does this collection belong to? This is the primary intellectual access point.
1. What is the title of this collection? This is a secondary intellectual access point.
1. What is the publication date of this collection? This is a secondary intellectual acess point.
1. Who is the creator of this collection? This a secondary intellectual access point.
1. Where can I find a representation of this unit? This is the primary access point.

We have to assume that there will be AT LEAST two types of metadata in the ldr metadata storage system.

1. Metadata about collections that belong to the University of Chicago Library and which all assets associated are in asset storage, e.g. OwnCloud
1. Metadata about collections that do not belong to the University of Chicago Library and which assets are stored elsewhere, e.g. Luna

This means that in order to provide a REQUIRED functionality, ldr metadata storage must be able to retrieve assets from either asset storage or any arbitrary outside storage accessible over the Web. It is therefore MANDATORY that all publicly available assets be available over the Web. However, the system must be able to distinguish between a remote asset and a library-controlled asset in order to know where to point clients for the location of assets. In order to distinguish between the two types of assets, there must be some marker for the ldr metadata storage to use to make this distinction. One marker will lead the ldr metadata storage to locate the assets from the digcoll retriever. The other will tell it to check if the address is valid. If the address is not valid, the ldr metadata storage should notify the administrators of the ldr metadata storage as well as the person attempting to ingest material into the ldr metadata storage. Any identifier that points to an asset controlled by the library MIST be a URI, because the ldr metadata storage must know from what host to pull the assets and we must assume that this host will change over time. Any identifier that points to a remote asset must be a URL. This is how the system will be able to distinguish what is a library-controlled asset and remote asset.

We also have to assume that there will be a variety of descriptive metadata formats used. These are the metadata formats currently being used in library digital collections.

- TEI
- EAD
- MODS
- VRACore
- OCR
- MARC

This means that the metadata storage must be able to store a variety of metadata formats that are not actionable by the metadata storage. However, the metadata storage must have a single schema that it can interpret in order to provide answers to the five questions defined earlier in this document.

COROLLARY: the metadata storage should be able to store technical metadata about assets in digital collections. Technical metadata is currently being stored in asset storage, but there is a strong argument to be made that doing this "muddies the water" between asset and metadata. Asset ought to be strictly defined as a byte stream representing an intellectual unit or some portion of an intellectual unit. By storing technical metadata, which by definition is not a byte stream representing a whole or some part of an intellectual unit but rather information about the byte stream the asset storage is being forced to perform a task that is a violation of its primary function.

## Contract for available endpoints

1. / = returns the endpoints available at the root of the API
1. /collections = returns a list of collections in the ldr metadata storage
1. /collections/[collection identifier/sub collection identifier/ sub-sub collection identifier] = returns a list of collections that are part of a particular collection [sub-collection, etc.]
1. /collection/[collection identifier] = returns the endpoints available for a particular collection
1. /collection/[collection identifier]/core = returns the core (metadata) describing a particular intellectual unit
1. /collection/[collection identifier]/extensions = returns a list of extension identifiers that are available for a particular collection
1. /collection/[collection identifier]/extensions/[extension identifier] = returns the extension metadata identified by the extension identifier that is available for a particular intellectual unit

## Contract for GET request responses from the ldr metadata storage

Every valid GET request to the ldr metadata is GUARANTEED to receive a well-formed XML or JSON response. This XML or JSON response will have the following information

- root element WILL be output
- output WILL have the following namespaces
  - ```http://lib.uchicago.edu/ldr``` which this document refers to with the shorthand ldr
  - ```http://www.w3.org/2001/XMLSchema-instance``` which this document refers to with the shorthand xsi
  - ```http://purl.org/dc/elements/1.1/``` which this document refers to with the shorthand dc
  - ```http://purl.org/dc/terms/``` which this document refers to with the shorthand dcterms
- the request that the ldr metadata storage received
- the date and time in ISO-8601 that the ldr metadata storage received that request WILL be the request timestamp from the timezone of the requestor
- the date and time in ISO-8601 that the ldr metadata storage sent the response from the timezone of the ldr metadata storage
- the type of response returned WILL be either aggregate or atomic
- the response in the form of the answer to the question asked by the request
- the response will be items if the response type is aggregate
- the response will be either metadata or extension if the response type is atomic
- items will contain an item for each result that is part of the answer to the question being asked
- the value of an item WILL ALWAYS be a URI resolvable by the ldr metadata storage
- metadata will contain dublin core metadata
- metadata WILL contain 2 instances of dc:title
- metadata MAY contain a dc:date
- metadata MAY contain a dc:description
- metadata MAY contain a dc:isPartOf
- dc:isPatOf will have an attribute xsi:type with value dcterms:URI
- metadata MAY contain a dc:relation
- metadata MAY contain AT LEAST one dc:identifier
- dc:identifier WILL have an attribute xsi:type
- the attribute xsi:type on dc:identifier WILL either have have dcterms:URI OR dcterms:URL

See the example below for further guidance on what to expect from a GET request to the ldr metadata storage

```xml
<?xml version="1.0" encoding="utf-8"?>
<output>
    <request>/collections/campub</request>
    <requestReceivedTimeStamp>2017-07-28T14:02:12-06:00</requestReceivedTimeStamp>
    <responseSentTimeStamp>2017-07-28T14:02:17+07:00</responseSentTimeStamp>
    <responseType>aggregate</responseType>
    <response>
        <items>
            <item>/unit/mvol-0001-0002-0003</item>
            <item>/unit/mvol-0001-0002-0004</item>
            <item>/unit/mvol-0001-0002-0005</item>
            <item>/unit/mvol-0002-0001-0001</item>
            <item>/unit/mvol-0002-0001-0002</item>
            <item>/unit/mvol-0004-1918-0204</item>
        </item>
    </response>
</output>
```

```xml
<?xml version="1.0" encoding="utf-8"?>
<output>
    <request>/units/mvol-0001-0002-0004/core</request>
    <requestReceivedTimeStamp>2017-07T12:02:44-06:00</requestReceivedTimeStamp>
    <responseSentTimeStamp>2017-07-28T12:02:58+03:00</responseSentTimeStamp>
    <responseType>atomic</responseType>
    <response>
        <data>
            <metadata
                xmlns="http://lib.uchicago.edu/ldr"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xmlns:dc="http://purl.org/dc/elements/1.1/"
                xmlns:dcterms="http://purl.org/dc/terms/">
                <dc:title>Cap and Gown volume 2, issue 4</dc:title>
                <dc:date>1900-02-01</dc:date>
                <dc:creator>University of Chicago</dc:creator>
                <dc:title>Cap and Gown Volume 2, Issue 4</dc:title>
                <dc:identifier>mvol-0001-0002-0004</dc:identifier>
                <dc:isPartOf xsi:type="dcterms:URI">/collections/mvol/0001/0002</dc:identifier>
                <dci:hasPart xsi:type=="dcterms:URL">http://digcollretriever.lib.uchicago.edu/mvol-0001-002-0004/pdf</dc:hasPart>
                <dc:hasPart xsi:type=="dcterms:URL">http://digcollretriever.lib.uchicago.edu/mvol-0001-002-0004/metadata</dc:hasPart>
                <dc:hasPart xsi:type=="dcterms:URL">http://digcollretriever.lib.uchicago.edu/mvol-0001-002-0004/jejocr</dc:hasPart>
                <dc:hasPart xsi:type=="dcterms:URL">http://digcollretriever.lib.uchicago.edu/mvol-0001-002-0004_0001</dc:hasPart>
                <dc:hasPart xsi:type=="dcterms:URL">http://digcollretriever.lib.uchicago.edu/mvol-0001-002-0004_0002</dc:hasPart>
                <dc:hasPart xsi:type=="dcterms:URL">http://digcollretriever.lib.uchicago.edu/mvol-0001-002-0004_0003</dc:hasPart>
                <dc:hasPart xsi:type=="dcterms:URL">http://digcollretriever.lib.uchicago.edu/mvol-0001-002-0004_0004</dc:hasPart>
            <metadata>
        </data>
    </response>
</output>
```

```xml
<?xml version="1.0" encoding="utf-8"?>
<output xmlns="http://lib.uchicago.edu/ldr"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:dcterms="http://purl.org/dc/terms/">
    <request>/collections/mvol</request>
    <requestReceivedTimeStamp>2017-07T12:02:44-06:00</requestReceivedTimeStamp>
    <responseSentTimeStamp>2017-07-28T12:02:58+03:00</responseSentTimeStamp>
    <responseType>aggregate</responseType>
    <response>
        <items>
            <item>/collection/mvol/0001</item>
            <item>/collection/mvol/0001/0002</item>
            <item>/collection/mvol/0001/0002/0004</item>
        </items>
    </response>
</output>
```

```xml
<?xml version="1.0" encoding="utf-8"?>
<output>
    <request>/collection/mvol-0001/core</request>
    <requestReceivedTimeStamp>2017-07T12:02:44-06:00</requestReceivedTimeStamp>
    <responseSentTimeStamp>2017-07-28T12:02:58+03:00</responseSentTimeStamp>
    <responseType>atomic</responseType>
    <response>
        <data>
            <metadata
                xmlns="http://lib.uchicago.edu/ldr"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xmlns:dc="http://purl.org/dc/elements/1.1/"
                xmlns:dcterms="http://purl.org/dc/terms/">
                <dc:title>Cap and Gown</dc:title>
                <dc:identifier>mvol-0001</dc:identifier>
                <dc:isPartOf xsi:type="dcterms:URI">/collections/mvol</dc:identifier>
            <metadata>
        </data>
    </response>
</output>
```

```xml
<?xml version="1.0" encoding="utf-8"?>
<output>
    <request>/collection/mvol-0001-0002/core</request>
    <requestReceivedTimeStamp>2017-07T12:02:44-06:00</requestReceivedTimeStamp>
    <responseSentTimeStamp>2017-07-28T12:02:58+03:00</responseSentTimeStamp>
    <responseType>atomic</responseType>
    <response>
        <data>
            <metadata
                xmlns="http://lib.uchicago.edu/ldr"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xmlns:dc="http://purl.org/dc/elements/1.1/"
                xmlns:dcterms="http://purl.org/dc/terms/">
                <dc:title>Cap and Gown Volume 2</dc:title>
                <dc:identifier>mvol-0001-0002</dc:identifier>
                <dc:isPartOf xsi:type="dcterms:URI">/collections/mvol/0001</dc:identifier>
            <metadata>
        </data>
    </response>
</output>
```

```xml
<?xml version="1.0" encoding="utf-8"?>
<output>
    <request>/collection/mvol-0002-0004/core</request>
    <requestReceivedTimeStamp>2017-07T12:02:44-06:00</requestReceivedTimeStamp>
    <responseSentTimeStamp>2017-07-28T12:02:58+03:00</responseSentTimeStamp>
    <responseType>atomic</responseType>
    <response>
        <data>
            <metadata
                xmlns="http://lib.uchicago.edu/ldr"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xmlns:dc="http://purl.org/dc/elements/1.1/"
                xmlns:dcterms="http://purl.org/dc/terms/">
                <dc:title>Cap and Gown Volume 2, Issue 4</dc:title>
                <dc:identifier>mvol-0001-0002-0004</dc:identifier>
                <dc:isPartOf xsi:type="dcterms:URI">/collections/mvol/0001/0002</dc:identifier>
                <dci:hasPart xsi:type=="dcterms:URL">http://digcollretriever.lib.uchicago.edu/mvol-0001-002-0004/pdf</dc:hasPart>
                <dc:hasPart xsi:type=="dcterms:URL">http://digcollretriever.lib.uchicago.edu/mvol-0001-002-0004/metadata</dc:hasPart>
                <dc:hasPart xsi:type=="dcterms:URL">http://digcollretriever.lib.uchicago.edu/mvol-0001-002-0004/jejocr</dc:hasPart>
                <dc:hasPart xsi:type=="dcterms:URL">http://digcollretriever.lib.uchicago.edu/mvol-0001-002-0004_0001</dc:hasPart>
                <dc:hasPart xsi:type=="dcterms:URL">http://digcollretriever.lib.uchicago.edu/mvol-0001-002-0004_0002</dc:hasPart>
                <dc:hasPart xsi:type=="dcterms:URL">http://digcollretriever.lib.uchicago.edu/mvol-0001-002-0004_0003</dc:hasPart>
                <dc:hasPart xsi:type=="dcterms:URL">http://digcollretriever.lib.uchicago.edu/mvol-0001-002-0004_0004</dc:hasPart>
            <metadata>
        </data>
    </response>
</output>
```

## Contract for POST submissions to the ldr metadata storage

Every POST submission to the ldr metadata storage MUST be well-formed XML or JSON and be UTF-8 encoded. In addition, the information being submitted MUST conform to specific formatting requirements as will be defined for each piece of information that requirements are relevant.

- Where a collection identifier is submitted it MUST not exist in the ldr metadata storage before submission occurs
- The root element MUST be input
- The element input MUST have the following namespaces
  - ```http://lib.uchicago.edu/ldr``` which this document refers to with the shorthand ldr
  - ```http://www.w3.org/2001/XMLSchema-instance``` which this document refers to with the shorthand xsi
  - ```http://purl.org/dc/elements/1.1/``` which this document refers to with the shorthand dc
  - ```http://purl.org/dc/terms/``` which this document refers to with the shorthand dcterms
- There MUST be ONLY one instance of the element requestSentTimeStamp
- The value of requestSentTimeStamp MUST be valid ISO-8601
- There MUST be an element request
- The value of request MUST be the URI being requested
- There MUST be ONLY one instance of the element metadata beneath input
- There MUST be ONLY one instance of the element core beneath input
- There MUST be only one instance of the element metadata beneath the element core
- The element metadata MUST be a complex element
- There MUST be AT LEAST one instance of element dc:title beneath metadata
- There MAY be a requirement for a second instance of dc:title
- If there is a requirement for a second instance of dc:title than the value of that instance MUST be a single word comprised ONLY of alphanumeric ASCII characters
- There MAY be a requirement for a MANDATORY instance of dc:date beneath metadata
- If there is a requirement of an instance of dc:date than the value of that instance MUST be valid ISO-8601
- There may be a requirement that there MUST be AT LEAST one instance of dc:relation beneath metadata
- If there is a requirement for AT LEAST one instance of dc:relation than each instance MUST have an attribute xsi:type which MUST have a value of dcterms:URI
- If there is a requirement for AT LEAST one instance of dc:relation than each instance MUST have a value that is resolvable over HTTP to a resource in ldr metadata storage
- There MAY be a requirement for ONLY one instance of dc:description beneath metadata
- If there is a requirement for ONLY one instance of dc:description than the value of that instance MUST be text
  - GUIDELINE: In order to ensure easy display on a variety of screen sizes for hardware it is advised to keep to a limit of at most 4 sentences.
- There MUST be AT LEAST one instance of dc:identifier beneath metadata
- dc:identifier MUST have an attribute xsi:type which MUST have a value of either a.) dcterms:URI or b.) dcterms:URL
- dc:identifier MUST have a value that is resolvable over HTTP to an asset
- There MAY be a requirement there MUST be ONLY one instance of extensions beneath input
- If there is a requirement that MUST be ONLY one instance of extensions than there MUST be AT LEAST one instance of extension beneath extensions
- If there is a requirement for AT LEAST one instance of extension than there MUST be ONLY one instance of type beneath extension
- If there is a requirement for ONLY one instance type than the value of that instance MUST be xml
- If there is a requirement for AT LEAST one instance of extension than there MUST be ONLY one instance of name beneath extension
- If there is a requirement for an instance of name than the value of name MUST be an a single word consisting exclusively of alphabetic characters
- If there is a requirement for AT LEAST one instance of extension than there MUST be ONLY one instance of data element beneath extension
- If there is a requirement for ONLY one instance of data than there a root element of some extension metadata beneath that instance
- Any additional element added to the POST request that is not defined by the rules for a particular POST request will be considered a violation of the contract and cause for rejection

```xml
<?xml version="1.0" encoding="utf-8"?>
<input>
    <request>/collections/campub</request>
    <requestSentTimeStamp>2017-07-02T11:14:55-06:00<requestSentTimeStamp>
    <core>
        <metadata
        xmlns="http://lib.uchicago.edu/ldr"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:dcterms="http://purl.org/dc/terms/">
            <dc:title>[a long form and formal title of the collection e.g. Richard G. Maynard Papers. Digital Collection]</dc:title>
            <dc:title>[a short form one-word title of the collection that can be used as the identifier for the collection e.g. maynard]</dc:title>
            <dc:description>[1-4 sentences describing how this collection is significant to the library]</dc:description>
        </metadata>
    </core>
</input>
```

```xml
<?xml version="1.0" encoding="utf-8"?>
<input>
    <request>/unit/remote-collection-book1</request>
    <requestSentTimeStamp>2017-07-02T11:14:55-06:00<requestSentTimeStamp>
    <core>
        <metadata
        xmlns="http://lib.uchicago.edu/ldr"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:dcterms="http://purl.org/dc/terms/">
            <dc:title>This is a title</dc:title>
            <dc:creator>Doe, John</dc:title>
            <dc:date>1980-02-16</dc:date>
            <dc:identifier xsi:type="dcterms:URL">http://wwww.example.com/book1.pdf</dc:identifer>
            <dc:relation xsi:type="URI">/collections/campub</dc:relation>
        </metadata>
    </core>
</input>
```

```xml
<?xml version="1.0" encoding="utf-8"?>
<input>
    <request>/unit/mvol-0001-0002-0004</request>
    <requestSentTimeStamp>2017-07-02T11:14:55-06:00<requestSentTimeStamp>
    <core>
        <metadata
        xmlns="http://lib.uchicago.edu/ldr"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:dcterms="http://purl.org/dc/terms/">
            <dc:title>This is a title</dc:title>
            <dc:creator>John Doe</dc:title>
            <dc:date>1980-02-16</dc:date>
            <dc:identifier xsi:type="dcterms:URI">/mvol-0001-0002-0004</dc:identifier>
            <dc:relation xsi:type="dcterms:URI">/collections/campub</dc:relation>
        </metadata>
    </core>
</input>
```

```xml
<?xml version="1.0" encoding="utf-8"?>
<input>
    <request>/unit/mvol-0001-0002-0004</request>
    <requestSentTimeStamp>2017-07-02T11:14:55-06:00<requestSentTimeStamp>
    <core>
        <metadata
        xmlns="http://lib.uchiago.edu/ldr"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:dcterms="http://purl.org/dc/terms/">
            <dc:title>This is a title</dc:title>
            <dc:creator>John Doe</dc:title>
            <dc:date>1980-02-16</dc:date>
            <dc:identifier xsi:type="dcterms:URI">/mvol-0001-0002-0004</dc:identifier>
            <dc:relation xsi:type="dcterms:URI">/collections/campub</dc:relation>
        </metadata>
    </core>
    <extensions>
        <extension>
            <type>xml</type>
            <name>VRACore</name>
            <data>
                <!-- insert VRACore metadata record here -->
            </data>
        </extension>
        <extension>
            <type>xml</type>
            <name>alto</name>
            <data>
                <!-- insert alto metadata record here -->
            </data>
        </extension>
    </extensions>
</input>
```

## Requirements for the metadata storage system

## Descriptions of endpoints

### /

communication protocol: Web

communication methods: GET

This endpoint is GUARANTEED to return a list of contexts available from the root of the API.

### /collections

communication protocols: Web

communication methods: GET

The GET method for this endpoint is GUARANTEED to return an up-to-date list of collections.

- request: /collections
- requestReceivedTimeStamp: [ISO-8601 date and time]
- responseSentTimeStamp: [ISO-8601 date and time]
- responseType: aggregate
- response: contains items element and inside items an item element that contains a URI resolvable to a particular collection

### /collections/[collection identifier/sub-collection identifier/sub-sub-collection identifier]

communication protocols: Web

communication methods: GET, POST

The GET method for this endpoint is GUARANTEED to return an up-to-date list of units in the collection identified.

- request: /units/[collection identifier/sub-collection identifier/sub-sub-collection identifier]
- requestReceivedTimeStamp: [ISO-8601 date and time]
- responseSentTimeStamp: [ISO-8601 date and time]
- responseType: aggregate
- response: contains items element and inside items an item element that contains a URI resolvable to a particular collection

The POST method for this endpoint is GUARANTEED to accept and save a new collection if the POST data obeys the CONTRACT for POST data.

- collection title and identifier do not exist in the ldr metadata storage prior to submission of the POST request
- There MUST be ONLY two dc:title elements
- There MUST be ONLY one dc:description element
- See Contract for POST submissions to the ldr metadata storage section for how to interpret these specific rules

### /collection/[collection identifier]

communication protocol: Web

communication methods: GET, POST

The GET method for this endpoint is GUARANTEED to return a list of endpoints available for the collection identified

- request: /collection/[collection identifer]
- requestReceivedTimeStamp: [ISO-8601 date and time]
- responseSentTimeStamp: [ISO-8601 date and time]
- responseType: atomic
- response: contains items element and inside items an item element that contains a URI resolvable to a particular endpoint available from the endpoint for this collection

The POST method for this endpoint is GUARANTEED to accept and save a new collection if the POST data obeys the CONTRACT for POST data.

- the collection is unique to the ldr metadata storage system
- There MUST be ONLY one dc:title elements
- There MUST be AT LEAST one dc:relation element
- There MUST be AT LEAST one dc:identifier element
- There MUST be ONLY one dc:date element
- There MAY be ONLY one extensions element
- See Contract for POST submissions to the ldr metadata storage section for how to interpret these specific rules

### /collection/[collection identifier]/core

communication protocol: Web

communication methods: GET

error conditions: no "core" resource available

This endpoint is GUARANTEED to return the core metadata for the collection identified.

- request: /collection/[collection identifer]/core
- requestReceivedTimeStamp: [ISO-8601 date and time]
- responseSentTimeStamp: [ISO-8601 date and time]
- responseType: atomic
- response: contains metadata element and inside metadata element is the core metadata for this particular collection

### /collection/[collection identifier]/extensions

communication protocol: Web

communication methods: GET

error conditions: no extensions available

This endpoint is GUARANTEED to return a listing of all extension resources available for the collection identified.

- request: /collection/[intellectual unit identifer]/extensions
- requestReceivedTimeStamp: [ISO-8601 date and time]
- responseSentTimeStamp: [ISO-8601 date and time]
- responseType: aggregate
- response: contains items element and inside items an item element that contains a URI resolvable to a particular extension endpoint available for this particular collection

### /collection/[collection identifier]/extensions/[extension identifier]

communication protocol: Web

communication methods: GET

error conditions: extension requested does not exist

This endpoint is GUARANTEED to return a particular extension resource identified by extension identifier that is available to describe the collection identified by collection identifier.

- request: /collection/[collection identifer]/extensions/[extension identifer]
- requestReceivedTimeStamp: [ISO-8601 date and time]
- responseSentTimeStamp: [ISO-8601 date and time]
- responseType: atomic
- response: contains extension element and inside extension element is the extension metadata available at this extension identifier for the particular collection

## Glossary

- a collection is a group of collections or a group of assets
- asset is a byte stream representing an intellectual unit whether in-whole or in-part
- descriptive metadata represents one description of a collection
- metadata is an abbreviation of descriptive metadata
- endpoint is a particular context for metadata that will provide some functionality
- functionality is either a.) the answer to a particular question about a particular resource or b.) some action or set of actions that transforms the resource identified into something new for the client to consume
- field is a particular part of metadata. ex. title is a field
- core metadata (abbreviated "core") are the REQUIRED fields
- extension metadata (abbreviated "extension" or "extensions") are OPTIONAL descriptive metadata for an intellectual unit
- client is a program that is requesting metadata. A client may be acting on behalf of a biological being.
- technical metadata is technical information about an asset. This information may include but is not limited to width and height pixel dimensions of an image byte stream or duration of a video file or size in disk storage required by a particular byte stream.
