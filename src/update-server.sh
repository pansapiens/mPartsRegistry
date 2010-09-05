#!/bin/sh
GAE_PATH=/data/python_devel/appengine/google_appengine/
APP_PATH=$(pwd)

# update the server on App Engine
python $GAE_PATH/appcfg.py --secure update $APP_PATH
