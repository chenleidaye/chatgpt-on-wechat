#!/bin/sh

# 用环境变量替换模板生成 config.json
envsubst < /app/plugins/config.template.json > /app/plugins/config.json

# 启动原程序
exec /entrypoint.sh "$@"
