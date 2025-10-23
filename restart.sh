#!/usr/bin/env bash
# restart.sh - Restart Python service by calling stop.sh + start.sh

set -Eeuo pipefail

# 必须指定环境参数，如 dev / prod
#if [ $# = 0 ]; then
#  echo "Please specify environment"
#  exit 1
#fi

# 获取脚本所在目录
APP_ENV="sv"
APP_HOME=$(dirname "$0")
APP_HOME=$(cd "$APP_HOME"; pwd)
APP_PID_FILE="$APP_HOME/$APP_ENV.pid"

echo "Restarting Python service [$APP_ENV] ..."

# 如果 PID 文件存在，则先停止旧进程
if [ -f "$APP_PID_FILE" ]; then
    echo "Stopping existing instance..."
    bash "$APP_HOME/shutdown.sh" || true
    sleep 5
fi

# 启动新进程
echo "Starting new instance..."
bash "$APP_HOME/startup.sh"

echo "Restarted successfully."
