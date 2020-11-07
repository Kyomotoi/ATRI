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
        group = str(event.group_id)

        # 名单目录
        file_user = Path('.') / 'utils' / 'utils_rule' / 'ban_list_user.json'
        file_group = Path('.') / 'utils' / 'utils_rule' / 'ban_list_group.json'

        # 检查文件是否存在，如不存在，自动创建并写入默认值
        if not file_user.is_file():
            file = open(file_user, 'w')
            file.write(json.dumps({}))
            file.close()

        if not file_group.is_file():
            file = open(file_group, 'w')
            file.write(json.dumps({}))
            file.close()

        # 读取文件
        with open(file_user, 'r') as f:
            data_user = json.load(f)

        with open(file_group, 'r') as f:
            data_group = json.load(f)

        # 判断目标
        if user:
            if user not in data_user:
                if group:
                    if group not in data_group:
                        return True
                    else:
                        return False
                else:
                    return True
            else:
                return False

        elif group:
            if group not in data_group:
                if user:
                    if user not in data_user:
                        return True
                    else:
                        return False
                else:
                    return True
            else:
                return False
        else:
            return False

    return Rule(_chech_banlist)


def check_switch(func_name: str) -> Rule:
    '''
    检查目标功能是否开启

    :return: bool
    '''
    async def _check_switch(bot: Bot, event: Event, state: dict) -> bool:
        # 获取目标信息
        group = str(event.group_id)

        # 文件目录
        file_switch_all = Path('.') / 'utils' / 'utils_rule' / 'switch.json'
        file_switch_alone = Path(
            '.') / 'ATRI' / 'data' / 'data_Group' / f'{group}' / 'switch.json'

        # 检查文件是否存在，如不存在，自动创建并写入默认值
        if not file_switch_all.is_file():
            data_switch_all = {}
            data_switch_all["anime-setu"] = "True"
            data_switch_all["anime-pic-search"] = "True"
            data_switch_all["anime-vid-search"] = "True"
            data_switch_all["ai-face"] = "True"
            data_switch_all["pixiv-pic-search"] = "True"
            data_switch_all["pixiv-author-search"] = "True"
            data_switch_all["pixiv-rank"] = "True"
            data_switch_all["one-key-adult"] = "True"

            file = open(file_switch_all, 'w')
            file.write(json.dumps(data_switch_all))
            file.close()

        if not file_switch_alone.is_file():
            data_switch_alone = {}

            # 检查目标文件夹是否存在，如不存在自动创建
            try:
                os.mkdir(
                    Path('.') / 'ATRI' / 'data' / 'data_Group' / f'{group}')

            data_switch_alone["anime-setu"] = "True"
            data_switch_alone["anime-pic-search"] = "True"
            data_switch_alone["anime-vid-search"] = "True"
            data_switch_alone["ai-face"] = "True"
            data_switch_alone["pixiv-pic-search"] = "True"
            data_switch_alone["pixiv-author-search"] = "True"
            data_switch_alone["pixiv-rank"] = "True"
            data_switch_alone["one-key-adult"] = "True"

            file = open(file_switch_alone, 'w')
            file.write(json.dumps(data_switch_alone))
            file.close()

        # 读取文件
        with open(file_switch_all, 'r') as f:
            data_all = json.load(f)

        with open(file_switch_alone, 'r') as f:
            data_alone = json.load(f)

        # 判断目标
        if data_all[func_name] == "True":
            if data_alone[func_name] == "True":
                return True
            else:
                return False
        else:
            await bot.send(event, f"Service-{func_name} has been closed.")
            return False

    return Rule(_check_switch)