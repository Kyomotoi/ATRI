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

import json
from pathlib import Path
from typing import Optional


def controlSwitch(func_name: str,
                  control: bool,
                  group: Optional[str] = None) -> str:
    '''
    控制开关 开启或关闭

    :return: str
    '''
    file_switch_all = Path('.') / 'ATRI' / 'utils' / 'utils_rule' / 'switch.json'

    if group:
        file_switch_group = Path(
            '.') / 'ATRI' / 'data' / 'data_Group' / f'{group}' / 'switch.json'
        try:
            with open(file_switch_group, 'r') as f:
                data_switch_group = json.load(f)
        except FileNotFoundError:
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


    with open(file_switch_all, 'r') as f:
        try:
            data_switch_all = json.load(f)
        except:
            data_switch_all = {}

    if not data_switch_all[f"{func_name}"]:
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