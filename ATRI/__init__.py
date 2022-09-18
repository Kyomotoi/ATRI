from time import sleep

import nonebot
from nonebot.adapters.onebot.v11 import Adapter

from .config import RUNTIME_CONFIG, BotSelfConfig, InlineGoCQHTTP

__version__ = "YHN-001-A07"


def asgi():
    return nonebot.get_asgi()


def driver():
    return nonebot.get_driver()


def init():
    nonebot.init(**RUNTIME_CONFIG)
    driver().register_adapter(Adapter)
    nonebot.load_plugins("ATRI/plugins")
    nonebot.load_plugins("ATRI/plugins/rss")
    if InlineGoCQHTTP.enabled:
        nonebot.load_plugin("nonebot_plugin_gocqhttp")
    sleep(3)


def run():
    log_level = "debug" if BotSelfConfig.debug else "warning"
    nonebot.run(log_level=log_level)
