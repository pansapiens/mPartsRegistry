#!/bin/sh
GAE_PATH=/data/python_devel/appengine/google_appengine/
APP_PATH=$(pwd)
ADDRESS=127.0.0.1
DB=dev_datastore
DB_HISTORY=dev_datastore.history

python $GAE_PATH/dev_appserver.py -a $ADDRESS --datastore_path=$DB --history_path=$DB_HISTORY $APP_PATH $*
