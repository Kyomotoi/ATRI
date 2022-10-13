from time import sleep
from pathlib import Path

import nonebot
from nonebot.adapters.onebot.v11 import Adapter

from .configs import Config

__version__ = "YHN-001-A07"
__conf_path = Path(".") / "config.yml"
__conf = Config(__conf_path)

conf = __conf.parse()


def asgi():
    return nonebot.get_asgi()


def driver():
    return nonebot.get_driver()


def init():
    nonebot.init(**__conf.get_runtime_conf())
    driver().register_adapter(Adapter)
    nonebot.load_plugins("ATRI/plugins")
    nonebot.load_plugins("ATRI/plugins/rss")
    if conf.WithGoCQHTTP.enabled:
        nonebot.load_plugin("nonebot_plugin_gocqhttp")
    sleep(3)


def run():
    log_level = "debug" if conf.BotConfig.debug else "warning"
    nonebot.run(log_level=log_level)
