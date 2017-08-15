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
- run ``bash ./debug.sh```
- open up your browser and navigate to ```http://localhost:5000/``` or open up a shell and call ```curl http://localhost:5000/```. It should return the following output:

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

See [wiki](https://github.com/uchicago-library/ldr_metadatastorage/wiki) for design specification.

Contributors:
- Brian Balsamo <bnbalsamo@uchicago.edu>
- Charles Blair <chas@uchicago.edu>
- Tyler Danstrom <tdanstrom@uchicago.edu>
