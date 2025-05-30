# encoding:utf-8

import os
import signal
import sys
import time
import requests

from channel import channel_factory
from common import const
from config import load_config
from plugins import *
import threading

class MCPClient:
    def __init__(self, base_url, token):
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def handle_user_message(message, mcp_client: MCPClient):
    if "搜索电影" in message:
        # 简单示例，提取电影名
        movie_name = extract_movie_name(message)  # 你自己写的提取逻辑
        media_info = mcp_client.search_media(movie_name)
        # 处理media_info，将结果发回微信用户
        reply_text = format_media_info(media_info)
        return reply_text
        
    def search_media(self, keyword, media_type="media"):
        url = f"{self.base_url}/search-media"
        data = {"keyword": keyword, "type": media_type}
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()

    def search_resources(self, mediaid, sites):
        url = f"{self.base_url}/search-media-resources"
        data = {"mediaid": mediaid, "sites": sites}
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()

def sigterm_handler_wrap(_signo):
    old_handler = signal.getsignal(_signo)

    def func(_signo, _stack_frame):
        logger.info("signal {} received, exiting...".format(_signo))
        conf().save_user_datas()
        if callable(old_handler):  #  check old_handler
            return old_handler(_signo, _stack_frame)
        sys.exit(0)

    signal.signal(_signo, func)


def start_channel(channel_name: str):
    channel = channel_factory.create_channel(channel_name)
    if channel_name in ["wx", "wxy", "terminal", "wechatmp","web", "wechatmp_service", "wechatcom_app", "wework",
                        const.FEISHU, const.DINGTALK]:
        PluginManager().load_plugins()

    if conf().get("use_linkai"):
        try:
            from common import linkai_client
            threading.Thread(target=linkai_client.start, args=(channel,)).start()
        except Exception as e:
            pass
    channel.startup()


def run():
    try:
        # load config
        load_config()
        # ctrl + c
        sigterm_handler_wrap(signal.SIGINT)
        # kill signal
        sigterm_handler_wrap(signal.SIGTERM)

        # create channel
        channel_name = conf().get("channel_type", "wx")

        if "--cmd" in sys.argv:
            channel_name = "terminal"

        if channel_name == "wxy":
            os.environ["WECHATY_LOG"] = "warn"

        start_channel(channel_name)

        while True:
            time.sleep(1)
    except Exception as e:
        logger.error("App startup failed!")
        logger.exception(e)


if __name__ == "__main__":
    run()
