from time import sleep

import nonebot as nb
from nonebot.adapters.cqhttp import Bot as ATRIBot

from .config import RUNTIME_CONFIG
from .log import logger


__version__ = "YHN-001-A01"


def asgi():
    return nb.get_asgi()


def driver():
    return nb.get_driver()


def init():
    nb.init(**RUNTIME_CONFIG)
    driver().register_adapter("cqhttp", ATRIBot)
    nb.load_plugins('ATRI/plugins')
    if RUNTIME_CONFIG["debug"]:
        nb.load_plugin("nonebot_plugin_test")
    logger.info(f"Now running: {__version__}")
    sleep(3)


def run(app):
    nb.run(app=app)
