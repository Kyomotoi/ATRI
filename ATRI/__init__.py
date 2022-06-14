from time import sleep

import nonebot
from nonebot.adapters.onebot.v11 import Adapter

from .config import RUNTIME_CONFIG, InlineGoCQHTTP
from .database import init_database

__version__ = "YHN-001-A05.fix1"


def asgi():
    return nonebot.get_asgi()


def driver():
    return nonebot.get_driver()


def init():
    nonebot.init(**RUNTIME_CONFIG)
    driver().register_adapter(Adapter)
    nonebot.load_plugins("ATRI/plugins")
    if InlineGoCQHTTP.enabled:
        nonebot.load_plugin("nonebot_plugin_gocqhttp")
    init_database()
    sleep(3)


def run():
    nonebot.run()
