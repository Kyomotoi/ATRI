#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   bot.py
@Time    :   2020/11/28 16:30:10
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2020 Kyomotoi, All Rights Reserved.
'''
__author__ = 'kyomotoi'

from check import CheckATRI

CheckATRI().checkConfig()
CheckATRI().checkRely()

import time
import nonebot
import datetime
from pathlib import Path
from ATRI.utils.utils_yml import load_yaml
from nonebot.log import default_format, logger

COPYRIGHT = (r"""====================[ATRI | アトリ]====================
* Mirai + NoneBot2 + Python
* Copyright © 2018-2020 Kyomotoi,All Rights Reserved
* Project: https://github.com/Kyomotoi/ATRI
* Blog: blog.lolihub.icu
=======================================================""")
print(COPYRIGHT)
time.sleep(1)

CONFIG_PATH = Path('.') / 'config.yml'
config = load_yaml(CONFIG_PATH)
config = config['bot']

LOGGER_INFO_PATH = Path(
    '.'
) / 'logs' / 'info' / f"{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}-INFO.log"
LOGGER_ERROR_PATH = Path(
    '.'
) / 'logs' / 'error' / f"{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}-ERROR.log"

nonebot.init(debug=bool(config['debug']),
             superusers=set(config['superusers']),
             nickname=set(config['nickname']),
             command_start=set(config['command_start']),
             command_sep=set(config['command_sep']))
app = nonebot.get_asgi()

nonebot.load_plugins('ATRI/plugins')

logger.add(LOGGER_INFO_PATH,
           rotation='10 MB',
           diagnose=False,
           level='INFO',
           format=default_format)

logger.add(LOGGER_ERROR_PATH,
           rotation='10 MB',
           diagnose=False,
           level='ERROR',
           format=default_format)

if __name__ == "__main__":
    logger.info("Running ATRI...")
    nonebot.run(app='bot:app', host=config['host'], port=config['port'])
