#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2020/11/07 14:33:22
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2020 Kyomotoi, All Rights Reserved.
'''
__author__ = 'kyomotoi'

import os
import json
import datetime
from pathlib import Path
from typing import Optional


def saveMessage(message_id: str,
                message: str,
                user: str,
                group: Optional[str] = None) -> None:
    """储存消息"""
    GROUP_PATH = Path(
        '.'
    ) / 'ATRI' / 'data' / 'data_Group' / f'{group}' / f"{datetime.datetime.now().strftime('%Y-%m-%d')}-message.json"
    PRIVATE_PATH = Path(
        '.'
    ) / 'ATRI' / 'data' / 'data_Private_Message' / f"{datetime.datetime.now().strftime('%Y-%m-%d')}-private-message.json"

    # 检查目标文件目录
    if not GROUP_PATH.is_file():
        try:
            os.mkdir(Path('.') / 'ATRI' / 'data' / 'data_Group' / f'{group}')
        except:
            pass

        with open(GROUP_PATH, 'w') as f:
            f.write(json.dumps({}))

    if not PRIVATE_PATH.is_file():
        try:
            os.mkdir(Path('.') / 'ATRI' / 'data' / 'data_Private_Message')
        except:
            pass

        with open(PRIVATE_PATH, 'w') as f:
            f.write(json.dumps({}))

    # 加载目标文件
    with open(GROUP_PATH, 'r') as f:
        DATA_GROUP = json.load(f)

    with open(PRIVATE_PATH, 'r') as f:
        DATA_PRIVATE = json.load(f)

    # 写入
    if group:
        DATA_GROUP[f"{message_id}"] = {
            "message": f"{message}",
            "user_id": f"{user}",
            "group_id": f"{group}"
        }

        with open(GROUP_PATH, 'w') as f:
            f.write(json.dumps(DATA_GROUP))

    else:
        DATA_PRIVATE[f"{message_id}"] = {
            "message": f"{message}",
            "user_id": f"{user}"
        }

        with open(PRIVATE_PATH, 'w') as f:
            f.write(json.dumps(DATA_PRIVATE))


def getMessage(message_id: str, group: Optional[str] = None) -> dict:
    '''
    传入消息id以获取对应信息
    
    :return: dict
    '''
    GROUP_PATH = Path(
        '.'
    ) / 'ATRI' / 'data' / 'data_Group' / f'{group}' / f"{datetime.datetime.now().strftime('%Y-%m-%d')}-message.json"
    PRIVATE_PATH = Path(
        '.'
    ) / 'ATRI' / 'data' / 'data_Private_Message' / f"{datetime.datetime.now().strftime('%Y-%m-%d')}-private-message.json"

    if group:
        try:
            with open(GROUP_PATH, 'r') as f:
                data_group = json.load(f)
            return data_group[message_id]

        except:
            return {"status": 0}

    else:
        try:
            with open(PRIVATE_PATH, 'r') as f:
                data_private = json.load(f)
            return data_private[message_id]

        except:
            return {"status": 0}
