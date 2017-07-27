# Introduction

This is a specification for how to get input into the metadata storage and how to get output from the metadata storage. As such, it will define a specification for how to add metadata to the metadata storage and the interface endpoints that the metadata storage will make available in order to receive input. It will also define the  endpoints that the metadata storage must make available to allow clients to access the metadata from the metadata storage, and the format that the output body will take.

# Input

```
{'identifier': [some identifier],
 'schema': [json ld-schema],
 'core': {
    'type': [book|article|;image|video|audio],
    'title': [how this intellectual unit is identiifed],
    'date': [when this intellectual unit was published],
    'identifier':[identifier for an asset in asset storage that represents this intellectual unit],
    'collections': [list of formal collection names that wil be used by ]

 },
 'extensions': [
     {
     'type':[xml|json]
     'schema':[namespace of xml schema that this is representative of]
     'data': [data encoded as base64],
    }
 ]
}
```

Th metadata storage will do the following on reception of the data

1. extract the core data and generate a dublin core record conforming to dublin core schema for 

