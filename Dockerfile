FROM ghcr.io/zhayujie/chatgpt-on-wechat:latest

# 安装 envsubst 所需的工具
RUN apk add --no-cache gettext

# 拷贝模板配置文件
COPY config.template.json /app/plugins/config.template.json

# 拷贝自定义入口脚本
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
