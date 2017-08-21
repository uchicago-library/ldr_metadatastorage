#!/bin/sh

APP_SAVE=$FLASK_APP
export FLASK_APP=metadatastorageapi
export FLASK_DEBUG=1
export METADATA_STORAGE_API_METADATA_FILE="C:/Users/tyler/Documents/Github/ldr_metadatastorage/sandbox/colections.xml"
python -m flask run -h localhost -p 5020
export FLASK_APP=$APP_SAVE