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
from pathlib import Path
from typing import Optional


def saveMessage(message_id: str,
                message: str,
                user: str,
                group: Optional[str] = None) -> None:
    """储存消息"""
    file_group = Path(
        '.') / 'ATRI' / 'data' / 'data_Group' / f'{group}' / 'message.json'
    file_private = Path(
        '.') / 'ATRI' / 'data' / 'data_Log' / 'message_private.json'

    try:
        with open(file_group, 'r') as f:
            data_group = json.load(f)
    except:
        data_group = {}

    try:
        with open(file_private, 'r') as f:
            data_private = json.load(f)
    except:
        data_private = {}

    if group:
        data_group[f"{message_id}"] = {
            "message": f"{message}",
            "user_id": f"{user}",
            "group_id": f"{group}"
        }

        try:
            with open(file_group, 'w') as f:
                f.write(json.dumps(data_group))
                f.close()
        except:
            os.mkdir(Path('.') / 'ATRI' / 'data' / 'data_Group' / f'{group}')
            with open(file_group, 'w') as f:
                f.write(json.dumps(data_group))
                f.close()
    else:
        data_private[f"{message_id}"] = {
            "message": f"{message}",
            "user_id": f"{user}"
        }

        try:
            with open(file_private, 'w') as f:
                f.write(json.dumps(data_private))
                f.close()
        except:
            os.mkdir(Path('.') / 'ATRI' / 'data' / 'data_Log')
            with open(file_private, 'w') as f:
                f.write(json.dumps(data_private))
                f.close()


def getMessage(message_id: str, group: Optional[str] = None) -> dict:
    '''
    传入消息id以获取对应信息
    
    :return: dict
    '''
    file_group = Path(
        '.') / 'ATRI' / 'data' / 'data_Group' / f'{group}' / 'message.json'
    file_private = Path(
        '.') / 'ATRI' / 'data' / 'data_Log' / 'message_private.json'

    if group:
        try:
            with open(file_group, 'r') as f:
                data_group = json.load(f)
            return data_group[message_id]

        except:
            return {"status": "None"}
    else:
        try:
            with open(file_private, 'r') as f:
                data_private = json.load(f)
            return data_private[message_id]

        except:
            return {"status": "None"}
