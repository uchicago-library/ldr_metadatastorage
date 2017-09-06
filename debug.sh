#!/bin/bash
echo "METADATA_STORAGE_API_STORAGE_TYPE: ${METADATA_STORAGE_API_STORAGE_TYPE}"
echo "METADATA_STORAGE_API_STORAGE_LOCATION: ${METADATA_STORAGE_API_STORAGE_LOCATION}"
APP_SAVE=$FLASK_APP
FLASK_APP=metadatastorageapi
python -m flask run
export FLASK_APP=$APP_SAVE
