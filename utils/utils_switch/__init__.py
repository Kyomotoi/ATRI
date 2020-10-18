#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2020/10/11 14:44:06
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

def checkSwitch(func_name: str, group: str) -> bool:
    """
    :说明:

      判断此功能针对 群 或 全体 是否开启。
    
    :参数:
    
      * ``func_name: str``: 功能名称
      * ``group: str``: 功能触发所在群号
    
    :返回:

      是：True | 否：False
    
    :用法:

    .. code-block:: python

        switch(func_name=Func, group=123456789)
    
    """
    file_switch_all = Path('.') / 'utils' / 'utils_switch' / 'switch.json'
    file_switch_alone = Path('.') / 'ATRI' / 'data' / 'data_Group' / f'{group}' / 'switch.json'

    try:
        with open(file_switch_all, 'r') as f:
            data_switch_all = json.load(f)
    except:
        data_switch_all = {}
        data_switch_all["anime-setu"] = "True"
        data_switch_all["anime-pic-search"] = "True"
        data_switch_all["anime-vid-search"] = "True"
        data_switch_all["ai-face"] = "True"
        data_switch_all["pixiv-pic-search"] = "True"
        data_switch_all["pixiv-author-search"] = "True"
        data_switch_all["pixiv-rank"] = "True"

        with open(file_switch_all, 'w') as f:
            f.write(json.dumps(data_switch_all))
            f.close()
    
    try:
        with open(file_switch_alone, 'r') as f:
            data_switch_alone = json.load(f)
    except:
        data_switch_alone = {}
        try:
            os.mkdir(Path('.') / 'ATRI' / 'data' / 'data_Group' / f'{group}')
        except:
            pass

        data_switch_alone["anime-setu"] = "True"
        data_switch_alone["anime-pic-search"] = "True"
        data_switch_alone["anime-vid-search"] = "True"
        data_switch_alone["ai-face"] = "True"
        data_switch_alone["pixiv-pic-search"] = "True"
        data_switch_alone["pixiv-author-search"] = "True"
        data_switch_alone["pixiv-rank"] = "True"

        with open(file_switch_alone, 'w') as f:
            f.write(json.dumps(data_switch_alone))
            f.close()

    if data_switch_all[func_name] == "True":
        if data_switch_alone[func_name] == "True":
            return True
        else:
            return False
    else:
        return False
    
def controlSwitch(func_name: str, control: bool, group: Optional[str] = None) -> str:
    """
    :说明:

      目标功能针对 群 或 全体 开启或关闭。
    
    :参数:
    
      * ``func_name: str``: 功能名称
      * ``control: bool``: 开启 / 关闭
      * ``group: Optional[str] = None``: 对应群号，若不传入则为全局
    
    :返回:

      None
    
    :用法:

    .. code-block:: python

        controlSwitch(func_name=Func, group=123456789)
    
    """
    file_switch_all = Path('.') / 'utils' / 'utils_switch' / 'switch.json'

    if group:
        file_switch_group = Path('.') / 'ATRI' / 'data' / 'data_Group' / f'{group}' / 'switch.json'
        try:
            with open(file_switch_group, 'r') as f:
                data_switch_group = json.load(f)
        except:
            data_switch_group = {}
        
        if data_switch_group[f"{func_name}"]:
            pass
        else:
            return f"Can't find func({func_name})"

        data_switch_group[f"{func_name}"] = f"{control}"

        with open(file_switch_group, 'w') as f:
            f.write(json.dumps(data_switch_group))
            f.close()

    else:
        pass

    try:
        with open(file_switch_all, 'r') as f:
            data_switch_all = json.load(f)
    except:
        data_switch_all = {}
    
    if data_switch_all[f"{func_name}"]:
        pass
    else:
        return f"Can't find func({func_name})"

    data_switch_all[f"{func_name}"] = f"{control}"

    with open(file_switch_all, 'w') as f:
        f.write(json.dumps(data_switch_all))
        f.close()

    if control == True:
        if group:
            msg = f"({func_name}) has been opened for group ({group})!"
        else:
            msg = f"({func_name}) has been opened!"
    
    else:
        if group:
            msg = f"({func_name}) has been closed for group ({group})!"
        else:
            msg = f"({func_name}) has been closed!"

    return msg