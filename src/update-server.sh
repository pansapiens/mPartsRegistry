#!/bin/sh
GAE_PATH=/data/code/google_appengine/

APP_PATH=$(pwd)

# update the server on App Engine
python $GAE_PATH/appcfg.py --secure update $APP_PATH
