#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
File: __init__.py
Created Date: 2021-03-07 11:22:06
Author: Kyomotoi
Email: Kyomotoiowo@gmail.com
License: GPLv3
Project: https://github.com/Kyomotoi/ATRI
--------
Last Modified: Sunday, 7th March 2021 3:01:51 pm
Modified By: Kyomotoi (kyomotoiowo@gmail.com)
--------
Copyright (c) 2021 Kyomotoi
'''

from time import sleep

import nonebot as nb
from nonebot.adapters.cqhttp import Bot as ATRIBot

from .config import RUNTIME_CONFIG
from .log import logger


__version__ = "YHN-001-A01"


def asgi():
    return nb.get_asgi()


def init():
    nb.init(**RUNTIME_CONFIG)
    driver = nb.get_driver()
    driver.register_adapter("cqhttp", ATRIBot)
    nb.load_plugins('ATRI/plugins')
    logger.info(f"Now running: {__version__}")
    sleep(3)


def run(app):
    nb.run(app=app)
