#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path
from typing import Optional

def banList(user: str, group: Optional[str] = None) -> bool:
    """
    :说明:

      判断某一 用户/群 是否处于封禁名单中。

    :参数:

      * ``user: str``: 用户QQ号
      * ``group: Optional[str] = None``: 用户所在群号，若不传入则只检测用户

    :返回:
      
      是：False | 否：True
    
    :用法:

    .. code-block:: python
      
        banList(user=123456789, group=123456789)

    """
    file_user = Path('.') / 'utils' / 'utils_banList' / 'banList_user.json'
    file_group = Path('.') / 'utils' / 'utils_banList' / 'banList_group.json'

    try:
        with open(file_user, 'r') as f:
            data_user = json.load(f)
    except:
        data_user = {}
    
    try:
        with open(file_group, 'r') as f:
            data_group = json.load(f)
    except:
        data_group = {}
    
    if user not in data_user:
        if group:
            if group not in data_group:
                return True
            else:
                return False
        else:
            return True
    else:
        print(3)
        return False