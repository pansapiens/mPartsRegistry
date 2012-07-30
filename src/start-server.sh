#!/bin/sh
GAE_PATH=/data/code/google_appengine/
APP_PATH=$(pwd)
ADDRESS=127.0.0.1
PORT=8080
DB=dev_datastore
DB_HISTORY=dev_datastore.history

python $GAE_PATH/dev_appserver.py -a $ADDRESS -p $PORT --datastore_path=$DB --history_path=$DB_HISTORY $APP_PATH $*
