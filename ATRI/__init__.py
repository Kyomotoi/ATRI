#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

'''
@File    :   __init__.py
@Time    :   2021/01/26 11:21:07
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2020 Kyomotoi, All Rights Reserved.
'''
__author__ = 'kyomotoi'

import shutil
from pathlib import Path

from .log import logger
from .config import check_config
from .service.send import Send
from main import driver


PLUGIN_INFO_PATH = Path('.') / 'ATRI' / 'data' / 'service' / 'plugins'

@driver.on_startup
async def startup_event() -> None:
    logger.info('アトリは、高性能ですから！')
    check_config()

@driver.on_shutdown
async def shutdown_event() -> None:
    logger.info('Thanks for using!')
    try:
        shutil.rmtree(PLUGIN_INFO_PATH)
    except:
        pass

@driver.on_bot_connect
async def az(bot):
    await Send.send_to_superuser('test')


from .exceptions import Error as Error
from .request import Request as Request
