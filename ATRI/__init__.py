from time import sleep

import nonebot
from nonebot.adapters.cqhttp import Bot as ATRIBot

from .config import RUNTIME_CONFIG
from .log import logger


__version__ = "YHN-001-A04"


def asgi():
    return nonebot.get_asgi()


def driver():
    return nonebot.get_driver()


def init():
    nonebot.init(**RUNTIME_CONFIG)
    driver().register_adapter("cqhttp", ATRIBot)
    nonebot.load_plugins("ATRI/plugins")
    if RUNTIME_CONFIG["debug"]:
        nonebot.load_plugin("nonebot_plugin_test")
    sleep(3)


def run(app):
    nonebot.run(app=app)
