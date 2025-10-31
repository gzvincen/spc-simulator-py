#!/usr/bin/env bash

#APP_HOME=$(dirname "$0")
#APP_HOME=$(cd "$APP_HOME"; pwd)

#echo "APP_HOME: $APP_HOME"
#bash "$APP_HOME/startup.sh"
#/usr/bin/expect -f $APP_HOME/update.exp $APP_HOME

SERVER="root@10.140.32.25"
PASS="root"
sshpass -p "$PASS" scp -r -o StrictHostKeyChecking=no .git $SERVER:/opt/spc-simulator-py/ && \

REMOTE_CMD="
cd /opt/spc-simulator-py &&
export http_proxy=http://10.140.32.80:7897 &&
export https_proxy=http://10.140.32.80:7897 &&
export all_proxy=socks5://10.140.32.80:7897 &&
echo '🌍 Proxy 已设置成功' &&
git fetch &&
git reset --hard origin/main &&
git pull &&
rm -rf /opt/spc-simulator-py/.git &&
echo '✅ 代码更新完成'
"
sshpass -p "$PASS" ssh -o StrictHostKeyChecking=no $SERVER "$REMOTE_CMD"
#sshpass -p "$PASS" ssh -o StrictHostKeyChecking=no $SERVER \
#    "cd /opt/spc-simulator-py && export http_proxy=http://10.140.32.80:7897 && export https_proxy=http://10.140.32.80:7897 && export all_proxy=socks5://10.140.32.80:7897 && echo '🌍 Proxy 已设置成功' && git fetch && git reset --hard origin/main && git pull && rm -rf /opt/spc-simulator-py/.git && echo '✅ 代码更新完成'"
