#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

'''
@File    :   __init__.py
@Time    :   2020/12/05 18:40:43
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2020 Kyomotoi, All Rights Reserved.
'''
__author__ = 'kyomotoi'

import nonebot
from nonebot.plugin import on_command
from nonebot.typing import Bot, Event
from nonebot.permission import SUPERUSER


bots = nonebot.get_bots()

testGetBot = on_command('获取bot', permission=SUPERUSER)

@testGetBot.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
    print(bots)
