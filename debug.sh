#!/bin/bash
FLASK_APP=metadatastorageapi
APP_SAVE=$FLASK_APP
python -m flask run --debugger
export FLASK_APP=$APP_SAVE
