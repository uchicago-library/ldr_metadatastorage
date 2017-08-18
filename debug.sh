#!/bin/sh

APP_SAVE=$FLASK_APP
export FLASK_APP=metadatastorageapi
export FLASK_DEBUG=1
python -m flask run -h localhost -p 5020
export FLASK_APP=$APP_SAVE