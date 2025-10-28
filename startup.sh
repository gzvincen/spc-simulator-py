#!/usr/bin/env bash

source /root/.bashrc
conda activate spc-simulator

set -Eeuo pipefail

APP_ENV="sv"
APP_HOME=$(dirname "$0")
APP_HOME=$(cd "$APP_HOME"; pwd)
APP_PID_FILE="$APP_HOME/$APP_ENV.pid"

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
export PYTHONPATH="$APP_HOME"
NACOS_NAMESPACE="$APP_ENV" && export NACOS_NAMESPACE

APP_LAUNCHER="$PYTHON_BIN -m app.main"

# 启动并记录 PID
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
