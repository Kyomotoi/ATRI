#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

'''
@File    :   __init__.py
@Time    :   2020/11/21 22:50:49
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2020 Kyomotoi, All Rights Reserved.
'''
__author__ = 'kyomotoi'

import json
from pathlib import Path

BAN_LIST_PATH = Path('.') / 'ATRI' / 'utils' / 'utils_rule' / 'ban_list_user.json'
with open(BAN_LIST_PATH, 'r') as f:
    data = json.load(f)


def ban(user: str) -> None:
    data[user] = user
    with open(BAN_LIST_PATH, 'w') as f:
        f.write(json.dumps(data))

def unban(user: str) -> None:
    del data[user]
    with open(BAN_LIST_PATH, 'w') as f:
        f.write(json.dumps(data))
