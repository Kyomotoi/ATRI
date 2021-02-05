#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

'''
@File    :   main.py
@Time    :   2021/02/02 15:51:44
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2021 Kyomotoi, All Rights Reserved.
'''
__author__ = 'kyomotoi'

from time import sleep
from os import get_terminal_size

import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot

from ATRI.log import logger
from ATRI.config import RUNTIME_CONFIG, COPYRIGHT, VERSION


try:
    width, height = get_terminal_size()
except OSError:
    width, height = 0, 0

nonebot.init(**RUNTIME_CONFIG)
app = nonebot.get_asgi()
driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)
nonebot.load_plugins('ATRI/plugins')


if __name__ == "__main__":
    logger.warning(
        '\n'.join(
            i.center(width) for i in COPYRIGHT.splitlines()
        )
    )
    logger.info(f"Now running: {VERSION}")
    sleep(3)
    nonebot.run(app='main:app')
