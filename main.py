#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2020/12/18 18:07:07
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2020 Kyomotoi, All Rights Reserved.
'''
__author__ = 'kyomotoi'

import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot

from ATRI.log import logger
from ATRI.config import NONEBOT_CONFIG, CheckConfig

copyright = ("""
====================[ATRI | アトリ]====================
* Mirai + NoneBot2 + Python
* Copyright © 2018-2020 Kyomotoi,All Rights Reserved
* Project: https://github.com/Kyomotoi/ATRI
* Docs: https://kyomotoi.github.io/ATRI/#
* Version: YHN-00A-001 
=======================================================""")

CheckConfig()

nonebot.init(**NONEBOT_CONFIG)
app = nonebot.get_asgi()
driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot) # type: ignore
nonebot.load_plugins('ATRI/plugins')

if __name__ == "__main__":
    logger.info(copyright)
    logger.info('Running ATRI...')
    nonebot.run(app='main:app')