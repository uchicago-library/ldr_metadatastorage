# README

[![Build Status](https://travis-ci.org/uchicago-library/ldr_metadatastorage.svg?branch=master)](https://travis-ci.org/uchicago-library/ldr_metadatastorage)

## Quickstart

### Prequesites

- python3.5
- pyvenv-3.5
- git

### Quickstart instructions

- create a python 3.5 virtualenv
- activate that virtualenv
- git clone this repository
- cd into the repo directory
- run python setup.py development
- chmod +x debug.sh
- run ``bash ./debug.sh```. It should return the following output:

```xml
<?xml version="1.0" encoding="utf-8"?>
<output xmlns="http://lib.uchicago.edu/ldr"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:dcterms="http://purl.org/dc/terms/">
    <request>/collection/mvol-0001-0002/core</request>
    <requestReceivedTimeStamp>2017-07T12:02:44-06:00</requestReceivedTimeStamp>
    <responseSentTimeStamp>2017-07-28T12:02:58+03:00</responseSentTimeStamp>
    <responseType>contextual</responseType>
    <response>
        <data>
            <metadation
                <dc:relation xsi:type="dcterms:URI">/collections</dc:relation>
            <metadata>
        </data>
    </response>
</output>
```


## Introduction

Metadata storage must be able to answer the following questions about an intellectual unit.

1. What collection(s) does this collection belong to? This is the primary intellectual access point.
1. What is the title of this collection? This is a secondary intellectual access point.
1. What is the publication date of this collection? This is a secondary intellectual acess point.
1. Who is the creator of this collection? This a secondary intellectual access point.
1. Where can I find a representation of this unit? This is the primary access point.

We have to assume that there will be AT LEAST two types of metadata in the ldr metadata storage system.

1. Metadata about collections that belong to the University of Chicago Library and which all byte streams associated are in asset storage, e.g. OwnCloud
1. Metadata about collections that do not belong to the University of Chicago Library and which byte streams are stored elsewhere, e.g. Luna

This means that in order to provide a REQUIRED functionality, ldr metadata storage must be able to retrieve byte streams from either asset storage or any arbitrary outside storage accessible over the Web. It is therefore MANDATORY that all publicly available byte streams be available over the Web. However, the system must be able to distinguish between a remote asset and a library-controlled asset in order to know where to point clients for the location of byte streams. In order to distinguish between the two types of byte streams, there must be some marker for the ldr metadata storage to use to make this distinction. One marker will lead the ldr metadata storage to locate the byte streams from the digcoll retriever. The other will tell it to check if the address is valid. If the address is not valid, the ldr metadata storage should notify the administrators of the ldr metadata storage as well as the person attempting to ingest material into the ldr metadata storage. Any identifier that points to an asset controlled by the library MIST be a URI, because the ldr metadata storage must know from what host to pull the byte streams and we must assume that this host will change over time. Any identifier that points to a remote asset must be a URL. This is how the system will be able to distinguish what is a library-controlled asset and remote asset.

We also have to assume that there will be a variety of descriptive metadata formats used. These are the metadata formats currently being used in library digital collections.

- TEI
- EAD
- MODS
- VRACore
- OCR
- MARC

This means that the metadata storage must be able to store a variety of metadata formats that are not actionable by the metadata storage. However, the metadata storage must have a single schema that it can interpret in order to provide answers to the five questions defined earlier in this document.

COROLLARY: the metadata storage should be able to store technical metadata about byte streams in digital collections. Technical metadata is currently being stored in asset storage, but there is a strong argument to be made that doing this "muddies the water" between asset and metadata. Asset ought to be strictly defined as a byte stream representing an intellectual unit or some portion of an intellectual unit. By storing technical metadata, which by definition is not a byte stream representing a whole or some part of an intellectual unit but rather information about the byte stream the asset storage is being forced to perform a task that is a violation of its primary function.

## Contract for available endpoints

1. / = returns the endpoints available at the root of the API
1. /collections = returns a list of collections in the ldr metadata storage
1. /collections/[collection identifier/sub collection identifier/ sub-sub collection identifier] = returns a list of collections that are part of a particular collection [sub-collection, etc.]
1. /collection/[collection identifier] = returns the endpoints available for a particular collection
1. /collection/[collection identifier]/core = returns the core (metadata) describing a particular intellectual unit
1. /collection/[collection identifier]/proxies = returns a list of proxy identifiers that are available for a particular collection
1. /collection/[collection identifier]/proxies/[proxy identifier] = returns the proxy metadata identified by the proxy identifier that is available for a particular intellectual unit

## About core metadata

Core metadata are REQUIRED fields. These fields is what allows the ldr metadata storage to answer all of the questions sets out at the beginning of this document in a cross-collection manner.

- dc:title MUST be present
- dc:identifier MUST be present
- dc:isPartof MUST be present if the collection is a subordinate to another collection
- dc:hasPart MUST be present if the collection is a superior to another collection or  to byte streams
- dc:description is OPTIONAL
- dc:relation is OPTIONAL
- dc:relation, dc:isPartOf and dc:hasPart MUST have attribute xsi:type
- attribute xsi:type MUST have a value of dcterms:URI if the value of the element is a path resolvable by ldr metadata storage
- attribute xsi:type MUST have a value of dcterms:URL if the value of the element is a path resolvable by a remote system

## About proxy metadata

There are no requirements for proxy metadata, only that when posted it is wrapped in an proxies/proxy element and that the type (xml, text or json) is defined and an identifier created.

## The different types of responses

The consuming client must be able to distinguish between the kinds of responses that the ldr metadata storage will provide. If the response is aggregate, it means the consuming client needs to know what collections are present in a particular location in the ldr metadata storage. If the response is atomic, it means the consuming client needs to know something in particular about a particular collection or proxy metadata. If the response is contextual, it means the consuming client needs to know where it can go next on its journey through the ldr metadata storage. In this way, the consuming client can navigate its way through the ldr metadata storage and be able to quickly interpret the responses based on a check for responseType to verify that the responseType is the kind of response it wants.

Regardless of type, every response will have certain characteristics in common. Each one will have

- it will have the following namespaces
  - ```http://lib.uchicago.edu/ldr``` which this document refers to with the shorthand ldr
  - ```http://www.w3.org/2001/XMLSchema-instance``` which this document refers to with the shorthand xsi
  - ```http://purl.org/dc/elements/1.1/``` which this document refers to with the shorthand dc
  - ```http://purl.org/dc/terms/``` which this document refers to with the shorthand dcterms
- a request field which will have a value of the request being asked of the system.
- a requestReceivedTimeStamp which will have a value of the date and time that the system received the request in ISO-8601
- a requestSentTimeStamp which will have a value of the date and time that the system completed processing the request in ISO-8601 and sent it to the consuming client
- a responseType which will have as a value a string that is either aggregate, atomic, or contextual
- a response body which will contain the metadata that is the answer to the request

### About aggregate type responses

An aggregate response is one that that the consuming client can assume will present a list of collections that match the request

The following endpoints are aggregate

- /collections
- /collections/[collection identifier][/sub-collection identifier]?
- /collection/[collection identifier]/proxies

The aggregate response body metadata will consist of at least one dc:hasPart with attribute xsi:type="dcterms:URI". The value of each dc:hasPart will be a URI for a collection (if any) that are direct subordinate to the collection being requested about or a URL for an asset that is directly subordinate to the collection.

#### Contract for aggregate responses

```xml
<?xml version="1.0" encoding="utf-8"?>
<output xmlns="http://lib.uchicago.edu/ldr"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:dcterms="http://purl.org/dc/terms/">
    <request>/collections/mvol</request>
    <requestReceivedTimeStamp>2017-07-28T14:02:12-06:00</requestReceivedTimeStamp>
    <responseSentTimeStamp>2017-07-28T14:02:17+07:00</responseSentTimeStamp>
    <responseType>aggregate</responseType>
    <response>
        <metadata>
            <dc:hasPart xsi:type="dcterms:URI">/collection/mvol/0001</dc:hasPart>
            <dc:hasPart xsi:type="dcterms:URI">/collection/mvol/0002</dc:hasPart>
            <dc:hasPart xsi:type="dcterms:URI">/collection/mvol/0004</dc:hasPart>
            <dc:hasPart xsi:type="dcterms:URI">/collection/mvol/0446</dc:hasPart>
        </metadata>
    </response>
</output>
```

```xml
<?xml version="1.0" encoding="utf-8"?>
<output xmlns="http://lib.uchicago.edu/ldr"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:dcterms="http://purl.org/dc/terms/">
    <request>/collections/mvol/0001</request>
    <requestReceivedTimeStamp>2017-07-28T14:02:12-06:00</requestReceivedTimeStamp>
    <responseSentTimeStamp>2017-07-28T14:02:17+07:00</responseSentTimeStamp>
    <responseType>aggregate</responseType>
    <response>
        <metadata>
            <dc:hasPart xsi:type="dcterms:URI">/collection/mvol/0001/0000</dc:hasPart>
            <dc:hasPart xsi:type="dcterms:URI">/collection/mvol/0001/0001</dc:hasPart>
            <dc:hasPart xsi:type="dcterms:URI">/collection/mvol/0001/0002</dc:hasPart>
            <dc:hasPart xsi:type="dcterms:URI">/collection/mvol/0001/0003</dc:hasPart>
        </metadata>
    </response>
</output>
```

```xml
<?xml version="1.0" encoding="utf-8"?>
<output xmlns="http://lib.uchicago.edu/ldr"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:dcterms="http://purl.org/dc/terms/">
    <request>/collections/mvol/0001/0003</request>
    <requestReceivedTimeStamp>2017-07-28T14:02:12-06:00</requestReceivedTimeStamp>
    <responseSentTimeStamp>2017-07-28T14:02:17+07:00</responseSentTimeStamp>
    <responseType>aggregate</responseType>
    <response>
        <metadata>
            <dc:hasPart xsi:type="dcterms:URI">/collection/mvol/0001/0003/0000</dc:hasPart>
            <dc:hasPart xsi:type="dcterms:URI">/collection/mvol/0001/0003/0001</dc:hasPart>
            <dc:hasPart xsi:type="dcterms:URI">/collection/mvol/0001/0003/0002</dc:hasPart>
            <dc:hasPart xsi:type="dcterms:URI">/collection/mvol/0001/0003/0003</dc:hasPart>
        </metadata>
    </response>
</output>
```

```xml
<?xml version="1.0" encoding="utf-8"?>
<output xmlns="http://lib.uchicago.edu/ldr"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:dcterms="http://purl.org/dc/terms/">
    <request>/collections/mvol/0001/0003/0001</request>
    <requestReceivedTimeStamp>2017-07-28T14:02:12-06:00</requestReceivedTimeStamp>
    <responseSentTimeStamp>2017-07-28T14:02:17+07:00</responseSentTimeStamp>
    <responseType>aggregate</responseType>
    <response>
        <metadata>
            <dc:hasPart xsi:type="dcterms:URL">http://digcollretriever.lib.uchicago.edu/mvol-0001-0003-0001/pdf</dc:hasPart>
            <dc:hasPart xsi:type="dcterms:URL">http://digcollretriever.lib.uchicago.edu/mvol-0001-0003-0001/jejocr</dc:hasPart>
            <dc:hasPart xsi:type="dcterms:URL">http://digcollretriever.lib.uchicago.edu/mvol-0001-0003-0001_0001/jpg</dc:hasPart>
            <dc:hasPart xsi:type="dcterms:URL">http://digcollretriever.lib.uchicago.edu/mvol-0001-0003-0001_0002/jpg</dc:hasPart>
            <dc:hasPart xsi:type="dcterms:URL">http://digcollretriever.lib.uchicago.edu/mvol-0001-0003-0001_0003/jpg</dc:hasPart>
            <dc:hasPart xsi:type="dcterms:URL">http://digcollretriever.lib.uchicago.edu/mvol-0001-0003-0001_0004/jpg</dc:hasPart>
        </metadata>
    </response>
</output>
```

```xml
<?xml version="1.0" encoding="utf-8"?>
<output xmlns="http://lib.uchicago.edu/ldr"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:dcterms="http://purl.org/dc/terms/">
    <request>/collections/mvol/0001/0003/0001/proxies</request>
    <requestReceivedTimeStamp>2017-07-28T14:02:12-06:00</requestReceivedTimeStamp>
    <responseSentTimeStamp>2017-07-28T14:02:17+07:00</responseSentTimeStamp>
    <responseType>aggregate</responseType>
    <response>
        <metadata>
            <dc:relation xsi:type="dcterms:URI">/collection/mvol-0001-0003-0001/proxies/structMetadata</dc:hasPart>
        </metadata>
    </response>
</output>
```

### About atomic responses

An atomic response is one that the consuming client can assume will be present a single descriptive metadata

The following endpoints are atomic:

- /collection/[collection identifier]/core
- /collection/[collection identifier]/proxies/[proxy identifier]

The atomic response body metadata will consist of the following

- one dc:identifier element the value of which is the primary access point for the collection
- one dc:title element the value of which is the primary intellectual secondary access point for the collection

In addition, the atomic response body may have the following

- at least one dc:hasPart which will point to either a collection or an asset which is a direct subordinate of the collection
- at least one dc:isPartOf which will point to a collection of which the collection is directly subordinate
- one dc:date which is a secondary intellectual access point
- one dc:creator which is a secondary intellectual access point
- one dc:description which which relays contextual semantic information about the collection to the biological being on whose behalf the consuming client is working

#### Contract for atomic responses

```xml
<?xml version="1.0" encoding="utf-8"?>
<output xmlns="http://lib.uchicago.edu/ldr"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:dcterms="http://purl.org/dc/terms/">
    <request>/collection/mvol-0001/core</request>
    <requestReceivedTimeStamp>2017-07T12:02:44-06:00</requestReceivedTimeStamp>
    <responseSentTimeStamp>2017-07-28T12:02:58+03:00</responseSentTimeStamp>
    <responseType>atomic</responseType>
    <response>
        <metadata>
            <dc:title>Cap and Gown</dc:title>
            <dc:identifier>mvol-0001</dc:identifier>
            <dc:isPartOf xsi:type="dcterms:URI">/collections/mvol</dc:isPartOf>
        <metadata>
    </response>
</output>
```

```xml
<?xml version="1.0" encoding="utf-8"?>
<output xmlns="http://lib.uchicago.edu/ldr"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:dcterms="http://purl.org/dc/terms/">
    <request>/collection/mvol-0001-0002/core</request>
    <requestReceivedTimeStamp>2017-07T12:02:44-06:00</requestReceivedTimeStamp>
    <responseSentTimeStamp>2017-07-28T12:02:58+03:00</responseSentTimeStamp>
    <responseType>atomic</responseType>
    <response>
         <metadata>
            <dc:title>Cap and Gown Volume 2</dc:title>
            <dc:identifier>mvol-0001-0002</dc:identifier>
            <dc:isPartOf xsi:type="dcterms:URI">/collections/mvol/0001</dc:iisPartOf>
        <metadata>
    </response>
</output>
```

```xml
<?xml version="1.0" encoding="utf-8"?>
<output xmlns="http://lib.uchicago.edu/ldr"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:dcterms="http://purl.org/dc/terms/">
    <request>/units/mvol-0001-0002-0004/core</request>
    <requestReceivedTimeStamp>2017-07T12:02:44-06:00</requestReceivedTimeStamp>
    <responseSentTimeStamp>2017-07-28T12:02:58+03:00</responseSentTimeStamp>
    <responseType>atomic</responseType>
    <response>
            <metadata>
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
    </response>
</output>
```

```xml
<?xml version="1.0" encoding="utf-8"?>
<output xmlns="http://lib.uchicago.edu/ldr"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:dcterms="http://purl.org/dc/terms/">
    <request>/collection/mvol-0001-0002-0004/proxies/structuralMetadata</request>
    <requestReceivedTimeStamp>2017-07T12:02:44-06:00</requestReceivedTimeStamp>
    <responseSentTimeStamp>2017-07-28T12:02:58+03:00</responseSentTimeStamp>
    <responseType>atomic</responseType>
    <response>
        <proxy>
            <dc:description>this is structural metadata information about mvol-0001-002-0004M</dc:description>
            <data>
                <!-- insert base64 of struct.txt file for mvol-0001-0002-0004 -->
            </data>
        </proxy>
    </response>
</output>
```

### About contextual responses

A contextual response is one that merely tells the client which endpoints can be discovered from the particular endpoint that the client is at. It is a form of wayfinding, as if the consuming client is on a forest trail and has reached a fork in the road.

The following endpoints are contextual

- /
- /collection/[collection identifier]

The contextual response body metadata will consist of the following

- at least one dc:relation element the value of which is an endpoint available to the endpoint being requested

#### Contract for contextual responses

```xml
<?xml version="1.0" encoding="utf-8"?>
<output xmlns="http://lib.uchicago.edu/ldr"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:dc="http://purl.org/dc/elements/1.1/"
        xmlns:dcterms="http://purl.org/dc/terms/">
    <request>/</request>
    <requestReceivedTimeStamp>2017-07T12:02:44-06:00</requestReceivedTimeStamp>
    <responseSentTimeStamp>2017-07-28T12:02:58+03:00</responseSentTimeStamp>
    <responseType>contextual</responseType>
    <response>
        <data>
            <metadata>
                <dc:relation xsi:type="dcterms:URI">/collections</dc:relation>
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
    <request>/collection/mvol-0001-0002/core</request>
    <requestReceivedTimeStamp>2017-07T12:02:44-06:00</requestReceivedTimeStamp>
    <responseSentTimeStamp>2017-07-28T12:02:58+03:00</responseSentTimeStamp>
    <responseType>contextual</responseType>
    <response>
        <data>
            <metadata>
                <dc:relation xsi:type="dcterms:URI">/collections/mvol-0001-0002/core</dc:relation>
                <dc:relation xsi:type="dcterms:URI">/collections/mvol-0001-0002/proxies</dc:relation>
            <metadata>
        </data>
    </response>
</output>
```

## About sending POST data

The ldr metadata storage has the functionality to allow clients to add new collections to the system.

The following endpoint accepts POST data

- /collection/[collection identifier]

The POST request will accept a submission that includes the following

- MANDATORY core metadata
- OPTIONAL proxy metadata

The POST submission data must conform to the following

- have a root field named input
- output will have the following namespaces
  - ```http://lib.uchicago.edu/ldr``` which this document refers to with the shorthand ldr
  - ```http://www.w3.org/2001/XMLSchema-instance``` which this document refers to with the shorthand xsi
  - ```http://purl.org/dc/elements/1.1/``` which this document refers to with the shorthand dc
  - ```http://purl.org/dc/terms/``` which this document refers to with the shorthand dcterms
- have a field core which contains metadata that follows the instructions for a /collection/[collection identifier]/core
- may have a field proxies which contains at least one proxy field which must a field data
- field data MUST contain base64 representation of a proxy metadata
- a proxy field may have a field dc:description

```xml
<?xml version="1.0" encoding="utf-8"?>
<input xmlns="http://lib.uchicago.edu/ldr"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:dc="http://purl.org/dc/elements/1.1/"
       xmlns:dcterms="http://purl.org/dc/terms/">
    <request>/collections/campub</request>
    <requestSentTimeStamp>2017-07-02T11:14:55-06:00<requestSentTimeStamp>
    <core>
        <metadata>
            <dc:title>Campus Publications Digital Collection</dc:title>
            <dc:identifier>campub</dc:identifier>
            <dc:description>This is a digital collection consisting of campus publications</dc:description>
        </metadata>
    </core>
</input>
```

```xml
<?xml version="1.0" encoding="utf-8"?>
<input xmlns="http://lib.uchicago.edu/ldr"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:dc="http://purl.org/dc/elements/1.1/"
       xmlns:dcterms="http://purl.org/dc/terms/">
    <request>/collection/remote-collection-book1</request>
    <requestSentTimeStamp>2017-07-02T11:14:55-06:00<requestSentTimeStamp>
    <core>
        <metadata>
            <dc:title>This is a title</dc:title>
            <dc:creator>Doe, John</dc:title>
            <dc:date>1980-02-16</dc:date>
            <dc:identifier>remote-collection-book1</dc:identifier>
            <dc:isPartOf xsi:type="URI">/collections/remote/book1</dc:isPartOf>
        </metadata>
    </core>
</input>
```

```xml
<?xml version="1.0" encoding="utf-8"?>
<input xmlns="http://lib.uchicago.edu/ldr"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:dc="http://purl.org/dc/elements/1.1/"
       xmlns:dcterms="http://purl.org/dc/terms/">
    <request>/collection/speculum-01204</request>
    <requestSentTimeStamp>2017-07-02T11:14:55-06:00<requestSentTimeStamp>
    <core>
        <metadata>
            <dc:title>This is a title</dc:title>
            <dc:creator>John Doe</dc:title>
            <dc:date>1980-02-16</dc:date>
            <dc:identifier>mvol-0001-0002-0004</dc:identifier>
            <dc:isPartOf xsi:type="dcterms:URI">/collection/mvol/0001/0002/0004</dc:relation>
            <dc:hasPart xsi:type:URL="dcterms:URL">http://digcollretriever.lib.uchicago/mvol-0001-0002-0004/pdf</dc:hasPart>
            <dc:hasPart xsi:type:URL="dcterms:URL">http://digcollretriever.lib.uchicago/mvol-0001-0002-0004_0001/jpg</dc:hasPart>
            <dc:hasPart xsi:type:URL="dcterms:URL">http://digcollretriever.lib.uchicago/mvol-0001-0002-0004_0002/jpg</dc:hasPart>
            <dc:hasPart xsi:type:URL="dcterms:URL">http://digcollretriever.lib.uchicago/mvol-0001-0002-0004_0003/jpg</dc:hasPart>
            <dc:hasPart xsi:type:URL="dcterms:URL">http://digcollretriever.lib.uchicago/mvol-0001-0002-0004_0004/jpg</dc:hasPart>
        </metadata>
    </core>
</input>
```

```xml
<?xml version="1.0" encoding="utf-8"?>
<input xmlns="http://lib.uchiago.edu/ldr"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:dc="http://purl.org/dc/elements/1.1/"
       xmlns:dcterms="http://purl.org/dc/terms/">
    <request>/unit/mvol-0001-0002-0004</request>
    <requestSentTimeStamp>2017-07-02T11:14:55-06:00<requestSentTimeStamp>
    <core>
        <metadata>
            <dc:title>This is a title</dc:title>
            <dc:creator>John Doe</dc:title>
            <dc:date>1980-02-16</dc:date>
            <dc:identifier xsi:type="dcterms:URI">/mvol-0001-0002-0004</dc:identifier>
            <dc:relation xsi:type="dcterms:URI">/collections/campub</dc:relation>
        </metadata>
    </core>
    <proxies>
        <proxy>
            <dc:description>[insert some description of how this proxy metadata is relevant to the core metadata that it is a proxy for]
            <data>
                <!-- insert base64 content here -->
            </data>
        </proxy>
    </proxies>
</input>
```

## Descriptions of endpoints

### /

communication protocol: Web

communication methods: GET

error conditions(s): None

This endpoint is GUARANTEED to return a list of contexts available from the root of the API.

### /collections

communication protocols: Web

communication methods: GET

error conditions(s): None

This endpoint is GUARANTEED to return an up-to-date list of collections.

- request: /collections
- requestReceivedTimeStamp: [ISO-8601 date and time]
- responseSentTimeStamp: [ISO-8601 date and time]
- responseType: aggregate
- response: contains items element and inside items an item element that contains a URI resolvable to a particular collection

### /collections/[collection identifier/sub-collection identifier/sub-sub-collection identifier]

communication protocols: Web

communication methods: GET

error condition(s): one or more collection identifiers in hierarchy does not exist

The GET method for this endpoint is GUARANTEED to return an up-to-date list of collections that are subordinate to the collection identified.

- request: /units/[collection identifier/sub-collection identifier/sub-sub-collection identifier]
- requestReceivedTimeStamp: [ISO-8601 date and time]
- responseSentTimeStamp: [ISO-8601 date and time]
- responseType: aggregate
- response: contains items element and inside items an item element that contains a URI resolvable to a particular collection

### /collection/[collection identifier]

communication protocol: Web

communication methods: GET, POST, PUT

error condition(s): no collection matching the identifier can be found

The GET method for this endpoint is GUARANTEED to return a list of endpoints available for the collection identified

- request: /collection/[collection identifer]
- requestReceivedTimeStamp: [ISO-8601 date and time]
- responseSentTimeStamp: [ISO-8601 date and time]
- responseType: aggregate
- response: contains items element and inside items an item element that contains a URI resolvable to a particular endpoint available from the endpoint for this collection

The POST method for this endpoint is GUARANTEED to create a new collection if the POST data obeys the CONTRACT for POST data.

- the collection is unique to the ldr metadata storage system
- There MUST be ONLY one dc:title elements
- There MUST be AT LEAST one dc:relation element
- There MUST be AT LEAST one dc:identifier element
- There MUST be ONLY one dc:date element
- There MAY be ONLY one proxies element
- See Contract for POST submissions to the ldr metadata storage section for how to interpret these specific rules

The PUT method for this endpoint is is GUARANTEED to modify the record for the collection identified. The only modification allowed is to add an extension to a collection.

- the collection must exist in the ldr metadata storage system
- there MAY be a ONLY one dc:description element which describes the importance of the new proxy metadata for the collection it is being added to
- there MUST be ONLY one ldr:data element which contains a base64 representation of the proxy metadata being added. This proxy metadata may be in any format: binary, text, json, xml, et cetera.
- See contract for POST submissions to the ldr metadata storage section for more information

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

### /collection/[collection identifier]/proxies

communication protocol: Web

communication methods: GET

error conditions: no proxies available

This endpoint is GUARANTEED to return a listing of all proxy resources available for the collection identified.

- request: /collection/[intellectual unit identifer]/proxies
- requestReceivedTimeStamp: [ISO-8601 date and time]
- responseSentTimeStamp: [ISO-8601 date and time]
- responseType: aggregate
- response: contains items element and inside items an item element that contains a URI resolvable to a particular proxy endpoint available for this particular collection

### /collection/[collection identifier]/proxies/[proxy identifier]

communication protocol: Web

communication methods: GET

error conditions: proxy requested does not exist

This endpoint is GUARANTEED to return a particular proxy resource identified by proxy identifier that is available to describe the collection identified by collection identifier.

- request: /collection/[collection identifer]/proxies/[proxy identifer]
- requestReceivedTimeStamp: [ISO-8601 date and time]
- responseSentTimeStamp: [ISO-8601 date and time]
- responseType: atomic
- response: contains proxy element and inside proxy element is the proxy metadata available at this proxy identifier for the particular collection

## Glossary

- a collection is a group of collections and/or byte streams
- asset is a byte stream representing an intellectual unit whether in-whole or in-part
- descriptive metadata represents one description of a collection
- metadata is an abbreviation of descriptive metadata
- endpoint is a particular context for metadata that will provide some functionality
- functionality is either a.) the answer to a particular question about a particular resource or b.) some action or set of actions that transforms the resource identified into something new for the client to consume
- field is a particular part of metadata. ex. title is a field
- core metadata (abbreviated "core") are the REQUIRED fields
- proxy metadata (abbreviated "proxy" or "proxies") are OPTIONAL descriptive metadata for an intellectual unit
- client is a program that is requesting metadata. A client may be acting on behalf of a biological being.
- technical metadata is technical information about an asset. This information may include but is not limited to width and height pixel dimensions of an image byte stream or duration of a video file or size in disk storage required by a particular byte stream.
