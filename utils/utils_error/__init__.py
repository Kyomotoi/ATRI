#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import string
from pathlib import Path
from random import sample
from typing import Optional
from datetime import datetime
from traceback import format_exc

from nonebot.rule import keyword

def errorRepo(repo_msg: Optional[str] = None) -> str:
    """
    :说明:

      返回错误堆栈。
    
    :参数:

      * ``repo_msg: Optional[str] = None``: 此错误发生时指定的错误信息，若不传入则返回 unknown
    
    :返回:

      错误信息
    
    :用法:
    
    .. code-block:: python

        try:
            ...
        except Exception:
            print(errorRepo(repo_msg="message"))
    
    """
    file_error = Path('.') / 'ATRI' / 'data' / 'data_Error' / 'error.json'
    try:
        with open(file_error, 'r') as f:
            data_error = json.load(f)
    except:
        data_error = {}
    
    key_error = ''.join(sample(string.ascii_letters + string.digits, 16))
    msg_error = f"{datetime.now()}\n"
    msg_error = f"{format_exc()}"
    data_error[f"{key_error}"] = f"{msg_error}"

    with open(file_error, 'w') as f:
        f.write(json.dumps(data_error))
        f.close()
    
    if repo_msg:
        pass
    else:
        repo_msg = 'unknown'
    
    msg0 = f'ERROR! Reason: [{repo_msg}]\n'
    msg0 += f'trackID: {key_error}\n'
    msg0 += "请使用[来杯红茶]功能以联系维护者\n"
    msg0 += "并附上 trackID"

    return msg0