#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from pathlib import Path
from typing import Optional

def saveMessage(message_id: str, message: str, user: str, group: Optional[str] = None) -> None:
    """
    :说明:
      
      获取信息并进行存储。
    :参数:

      * ``message_id: str``: 消息id
      * ``message: str``: 目标信息
      * ``user: str``: 发出用户
      * ``group: Optional[str] = None``: 发出群号，若不传入则归入私聊消息
    
    :返回:

      None

    :用法:

    .. code-block:: python

        getMessage(message='test', user=123456789, group=123456789)

    """
    file_group = Path('.') / 'ATRI' / 'data' / 'data_Group' / f'{group}' / 'message.json'
    file_private = Path('.') / 'ATRI' / 'data' / 'data_Log' / 'message_private.json'

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
        data_group[f"{message_id}"] = {"message": f"{message}", "user_id": f"{user}", "group_id": f"{group}"}
    
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
        data_private[f"{message_id}"] = {"message": f"{message}", "user_id": f"{user}"}

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
    """
    :说明:
    
      通过 message_id 获取到对应消息参数: message, user, group
    
    :参数:

      * ``message_id: str``: 目标消息id
      * ``group: Optional[str] = None``: 对应群号，若不传入则获取私聊消息
    
    :返回:

      消息内容，类型为: dict
    
    :用法:

    .. code-block:: python

        loadMessage(message_id=123456789)

    """
    file_group = Path('.') / 'ATRI' / 'data' / 'data_Group' / f'{group}' / 'message.json'
    file_private = Path('.') / 'ATRI' / 'data' / 'data_Log' / 'message_private.json'

    if group:
        try:
            with open(file_group, 'r') as f:
                data_group = json.load(f)
            return data_group

        except:
            return {"status": "None"}
    else:
        try:
            with open(file_private, 'r') as f:
                data_private = json.load(f)
            return data_private

        except:
            return {"status": "None"}