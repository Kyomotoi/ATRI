#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2020/11/06 19:27:00
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2020 Kyomotoi, All Rights Reserved.
'''
__author__ = 'kyomotoi'

import os
import json
from pathlib import Path
from nonebot.rule import Rule
from nonebot.typing import Bot, Event


def check_banlist() -> Rule:
    '''
    检查目标是否存在于封禁名单

    :return: bool
    '''
    async def _chech_banlist(bot: Bot, event: Event, state: dict) -> bool:
        # 获取目标信息
        user = str(event.user_id)

        # 名单目录
        BAN_LIST_USER_PATH = Path(
            '.') / 'ATRI' / 'utils' / 'utils_rule' / 'ban_list_user.json'

        # 检查文件是否存在，如不存在，自动创建并写入默认值
        if not BAN_LIST_USER_PATH.is_file():
            with open(BAN_LIST_USER_PATH, 'w') as f:
                f.write(json.dumps({}))

        # 读取文件
        with open(BAN_LIST_USER_PATH, 'r') as f:
            data_user = json.load(f)

        return user not in data_user

    return Rule(_chech_banlist)


def check_switch(func_name: str, notice: bool) -> Rule:
    '''
    检查目标功能是否开启

    :return: bool
    '''
    async def _check_switch(bot: Bot, event: Event, state: dict) -> bool:
        # 获取目标信息
        group = str(event.group_id)

        # 文件目录
        SWITCH_ALL_PATH = Path('.') / 'ATRI' / 'utils' / 'utils_rule' / 'switch.json'
        SWITCH_ALONE_PATH = Path(
            '.') / 'ATRI' / 'data' / 'data_Group' / f'{group}' / 'switch.json'

        # 检查文件是否存在，如不存在，自动创建并写入默认值
        if not SWITCH_ALL_PATH.is_file():
            with open(SWITCH_ALL_PATH, 'ws') as f:
                f.write(json.dumps({}))

        if not SWITCH_ALONE_PATH.is_file():
            try:
                os.mkdir(
                    Path('.') / 'ATRI' / 'data' / 'data_Group' / f'{group}')
            except:
                pass

            with open(SWITCH_ALONE_PATH, 'w') as f:
                f.write(json.dumps({}))

        # 读取文件
        with open(SWITCH_ALL_PATH, 'r') as f:
            data_all = json.load(f)

        with open(SWITCH_ALONE_PATH, 'r') as f:
            data_alone = json.load(f)

        # 判断目标是否存在于将要读取的文件，如不存在，写入
        # 此项举措是为了适应以后版本更新出现新插件的状况
        # 不至于每次都需要修改
        if func_name not in data_all:
            data_all[func_name] = "True"
            with open(SWITCH_ALL_PATH, 'w') as f:
                f.write(json.dumps(data_all))

        if func_name not in data_alone:
            data_alone[func_name] = "True"
            with open(SWITCH_ALONE_PATH, 'w') as f:
                f.write(json.dumps(data_alone))

        # 判断目标
        if data_all[func_name] == "True":
            if data_alone[func_name] == "True":
                return True
            else:
                return False
        else:
            if notice:
                await bot.send(event, f"Service-{func_name} has been closed.")
            return False

    return Rule(_check_switch)
