#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
File: config.py
Created Date: 2021-02-02 16:43:54
Author: Kyomotoi
Email: Kyomotoiowo@gmail.com
License: GPLv3
Project: https://github.com/Kyomotoi/ATRI
--------
Last Modified: Sunday, 7th March 2021 2:31:06 pm
Modified By: Kyomotoi (kyomotoiowo@gmail.com)
--------
Copyright (c) 2021 Kyomotoi
'''

from pathlib import Path
from datetime import timedelta
from ipaddress import IPv4Address

from .utils.yaml import load_yml


CONFIG_PATH = Path('.') / 'config.yml'
config = load_yml(CONFIG_PATH)
nonebot_config = config['BotSelfConfig']


RUNTIME_CONFIG = {
    "host": IPv4Address(nonebot_config.get('host', '127.0.0.1')),
    "port": int(nonebot_config.get('port', '8080')),
    "debug": bool(nonebot_config.get('debug', False)),
    "superusers": set(nonebot_config.get('superusers', ["1234567890"])),
    "nickname": set(
        nonebot_config.get(
            'nickname',
            ['ATRI', 'Atri', 'atri', '亚托莉', 'アトリ']
        )
    ),
    "command_start": set(nonebot_config.get('command_start', ['', '/'])),
    "command_sep": set(nonebot_config.get('command_sep', ['.'])),
    "session_expire_timeout": timedelta(
        nonebot_config.get('session_expire_timeout', 2)
    )
}
