#!/bin/bash

APP_SAVE=$FLASK_APP
FLASK_APP=metadatastorageapi
python -m flask run
export FLASK_APP=$APP_SAVE
