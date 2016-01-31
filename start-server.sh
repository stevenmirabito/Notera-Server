#!/bin/bash
# Starts the Notera API Server

HOME=/home/notera
VENVDIR=$HOME/.notera_api_env
APPDIR=/home/notera/api

cd $APPDIR
source $VENVDIR/bin/activate
/home/notera/.notera_api_env/bin/uwsgi --ini /home/notera/api/notera.ini
