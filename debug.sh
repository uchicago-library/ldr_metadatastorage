#!/bin/sh

APP_SAVE=$FLASK_APP
export FLASK_APP=metadatastorageapi
export FLASK_DEBUG=1
export METADATA_STORAGE_API_METADATA_FILE="/mnt/c/Users/tyler/Documents/Github/ldr_metadatastorage/sandbox/colections.xml"
python -m flask run
export FLASK_APP=$APP_SAVE
