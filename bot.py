#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   bot.py
@Time    :   2020/10/11 14:36:01
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2020 Kyomotoi, All Rights Reserved.
'''
__author__ = 'kyomotoi'

import time
import nonebot
import datetime
from pathlib import Path
from utils.utils_yml import load_yaml
from nonebot.log import default_format, logger

from check import checkATRI

# 版权说明
COPYRIGHT = (r"""====================[ATRI | アトリ]====================
* Mirai + NoneBot2 + Python
* Copyright © 2018-2020 Kyomotoi,All Rights Reserved
* Project: https://github.com/Kyomotoi/ATRI
* Blog: blog.lolihub.icu
=======================================================""")
print(COPYRIGHT)
time.sleep(1)

# 检查是否符合条件运行
checkATRI()

# 读取配置
CONFIG_PATH = Path('.') / 'config.yml'
config = load_yaml(CONFIG_PATH)
config = config['bot']

# 初始化
nonebot.init(debug=bool(config['debug']),
             superusers=set(config['superusers']),
             nickname=set(config['nickname']),
             command_start=set(config['command_start']),
             command_sep=set(config['command_sep']))
app = nonebot.get_asgi()

# 读取插件目录
nonebot.load_plugins('ATRI/plugins')

# 自定义 Logger
LOGGER_INFO_PATH = Path(
    '.'
) / 'logs' / 'info' / f"{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}-INFO.log"
LOGGER_ERROR_PATH = Path(
    '.'
) / 'logs' / 'error' / f"{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}-ERROR.log"

# 记录正常日志
logger.add(LOGGER_INFO_PATH,
           rotation='10 MB',
           diagnose=False,
           level='INFO',
           format=default_format)

# 记录报错日志
logger.add(LOGGER_ERROR_PATH,
           rotation='10 MB',
           diagnose=False,
           level='ERROR',
           format=default_format)

if __name__ == '__main__':
    nonebot.run(app='bot:app', host=config['host'], port=config['port'])
