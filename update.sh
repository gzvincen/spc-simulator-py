#!/usr/bin/env bash

APP_HOME=$(dirname "$0")
APP_HOME=$(cd "$APP_HOME"; pwd)

#echo "APP_HOME: $APP_HOME"
#bash "$APP_HOME/startup.sh"
/usr/bin/expect -f $APP_HOME/update.exp $APP_HOME
