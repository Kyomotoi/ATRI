#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

'''
@File    :   __init__.py
@Time    :   2021/01/26 11:21:07
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2021 Kyomotoi, All Rights Reserved.
'''
__author__ = 'kyomotoi'

import time
import shutil
from pathlib import Path

from .log import logger
from .config import check_config, RUNTIME_CONFIG
from .service.httppost import HttpPost
from main import driver


PLUGIN_INFO_PATH = Path('.') / 'ATRI' / 'data' / 'service' / 'plugins'

@driver.on_startup
async def startup_event() -> None:
    logger.info('アトリは、高性能ですから！')
    check_config()

@driver.on_shutdown
async def shutdown_event() -> None:
    logger.info('Thanks for using.')
    logger.debug('bot已关闭，正在清理插件信息...')
    try:
        shutil.rmtree(PLUGIN_INFO_PATH)
    except:
        repo = ('清理插件信息失败',
                '请前往 ATRI/data/service 下',
                '将 plugins 整个文件夹删除')
        logger.error(repo)
        time.sleep(10)
        pass

@driver.on_bot_connect
async def connect(bot):
    for super in RUNTIME_CONFIG['superusers']:
        await HttpPost.send_private_msg(
            int(super), 'WebSocket 成功连接，数据开始传输~！')

@driver.on_bot_disconnect
async def disconnect(bot):
    for super in RUNTIME_CONFIG['superusers']:
        try:
            await HttpPost.send_private_msg(int(super), 'WebSocket 貌似断开了呢...')
        except:
            logger.error('WebSocket 已断开，等待重连')


from .exceptions import Error as Error
from .request import Request as Request
