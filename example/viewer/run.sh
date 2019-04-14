#!/bin/bash

CUR_DIR=`pwd`

COMMIT=`git rev-parse --short HEAD`
HOST=`hostname`
DATE=`date +%Y%m%d`

APP=viewer.py

INI_PRE=default
INI=config/$INI_PRE".ini"

echo "COMMIT: $COMMIT"
echo "HOST: $HOST"
echo "DATE: $DATE"
echo "APP: $APP"
echo "INI: $INI"
echo "ARGS: $@"

RUN_DIR=""

python $APP -c $INI --tag $COMMIT"."$HOST --run_dir "$RUN_DIR" $@

