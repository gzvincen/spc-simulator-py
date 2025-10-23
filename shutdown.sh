#!/usr/bin/env bash

set -Eeuo pipefail

#if [ $# = 0 ]; then
#  echo "Usage: $0 <env>"
#  echo "Example: ./stop.sh dev"
#  exit 1
#fi

APP_ENV="sv"
APP_HOME=$(dirname "$0")
APP_HOME=$(cd "$APP_HOME"; pwd)
APP_PID_FILE="$APP_HOME/$APP_ENV.pid"

if [ ! -f "$APP_PID_FILE" ]; then
  echo "⚠️  No PID file found for [$APP_ENV]"
  exit 0
fi

read -ra pids < <(cat "$APP_PID_FILE") || true

if kill -0 "${pids[0]}" > /dev/null 2>&1; then
  echo "🛑 Stopping service [$APP_ENV] (pid: ${pids[0]}) ..."
  kill "${pids[0]}" || true
  sleep 2
  if kill -0 "${pids[0]}" > /dev/null 2>&1; then
    echo "⚠️  Force killing process ..."
    kill -9 "${pids[0]}" || true
  fi
else
  echo "⚠️  Process ${pids[0]} not running."
fi

rm -f "$APP_PID_FILE"
echo "✅ SPC Simulator Service [$APP_ENV] stopped."
