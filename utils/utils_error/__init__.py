#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2020/10/11 14:43:10
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2020 Kyomotoi, All Rights Reserved.
'''
__author__ = 'kyomotoi'

import json
import string
from pathlib import Path
from random import sample
from typing import Optional
from datetime import datetime
from traceback import format_exc

def errorRepo(repo_msg: Optional[str] = None) -> str:
    '''
    出错时返回错误堆栈

    :return: str 
    '''
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