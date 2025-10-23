#!/usr/bin/env bash

set -Eeuo pipefail

#if [ $# = 0 ]; then
#  echo "Usage: $0 <env>"
#  echo "Example: ./start.sh dev"
#  exit 1
#fi

APP_ENV="sv"
APP_HOME=$(dirname "$0")
APP_HOME=$(cd "$APP_HOME"; pwd)
APP_PID_FILE="$APP_HOME/$APP_ENV.pid"
#APP_LOG_DIR="$APP_HOME/logs"

# 日志目录检查
#if [ ! -d "$APP_LOG_DIR" ]; then
#  mkdir -p "$APP_LOG_DIR"
#fi

#APP_LOG_FILE="$APP_LOG_DIR/${APP_ENV}.log"

echo "🐍 Python Service SPC Simulator [$APP_ENV] Starting ... "

# 检查是否已运行
if [ -f "$APP_PID_FILE" ]; then
  read -ra pids < <(cat "$APP_PID_FILE") || true
  if kill -0 "${pids[0]}" > /dev/null 2>&1; then
    echo "⚠️  Service [$APP_ENV] already running as process ${pids[0]}"
    exit 0
  fi
fi

# Python 环境
PYTHON_BIN="${PYTHON_BIN:-python3}"
echo "⚠️  PYTHON_BIN [$PYTHON_BIN] "
# 项目启动命令（根据你的 main.py）
APP_LAUNCHER="$PYTHON_BIN -m app.main"

# 启动并记录 PID
#if nohup $APP_LAUNCHER > "$APP_LOG_FILE" 2>&1 < /dev/null &
#then
#  echo $! > "$APP_PID_FILE"
#  sleep 1
#  echo "✅ Service [$APP_ENV] STARTED (pid: $(cat $APP_PID_FILE))"
#  echo "📜 Log: $APP_LOG_FILE"
#else
#  echo "❌ Failed to start service [$APP_ENV]"
#  exit 1
#fi

read -ra nohupArgs < <(echo "$APP_LAUNCHER")
if nohup "${nohupArgs[@]}" > /dev/null 2>&1 < /dev/null &
then
  if echo $! > "$APP_PID_FILE"
  then
    sleep 1
    echo STARTED
  else
    echo FAILED TO WRITE PID
    exit 1
  fi
else
  echo SERVER DID NOT START
  exit 1
fi
