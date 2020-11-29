#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2020/11/07 14:20:08
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2020 Kyomotoi, All Rights Reserved.
'''
__author__ = 'kyomotoi'

import re
import random
from time import strftime
from datetime import datetime, timedelta

from nonebot.plugin import on_command
from nonebot.typing import Bot, Event

from ATRI.utils.utils_error import errorRepo
from ATRI.utils.utils_rule import check_banlist, check_switch
from .data_source import Generate, Genshin, Roll

plugin_name_0 = "one-key-adult"
generateID = on_command("我要转大人，一天打25小时游戏",
                        aliases={'虚拟身份', '一键成年', '登dua郎'},
                        rule=check_banlist()
                        & check_switch(plugin_name_0, True))


@generateID.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
    NAME, AREA = Generate().infoID()

    BIRTH_BEGIN = datetime(*[1980, 10, 10])  # type: ignore
    BIRTH_END = datetime(*[2002, 10, 10])  # type: ignore

    id_card_area = int(random.choice(list(AREA.keys())))
    id_card_area_name = AREA[str(id_card_area)]
    id_card_year_old = timedelta(
        days=random.randint(0, (BIRTH_END - BIRTH_BEGIN).days) + 1)
    id_card_birth_day = strftime("%Y%m%d",
                                 (BIRTH_BEGIN + id_card_year_old).timetuple())
    id_card_sex = random.choice([0, 1])
    id_card_name = random.choice(NAME[{0: "female", 1: "male"}[id_card_sex]])
    id_card_id = Generate().numberID(id_card_area, id_card_sex,
                                     id_card_birth_day)  # type: ignore

    msg0 = "恭喜，你已经成大人了！\n"
    msg0 += f"NumberID: {id_card_id}\n"
    msg0 += f"Sex: {'男' if id_card_sex == 1 else '女'}\n"
    msg0 += f"Name: {id_card_name} || Address: {id_card_area_name}\n"
    msg0 += "注: 1、以上信息根据国家公开标准生成，非真实信息。\n"
    msg0 += "      2、不适用于网易和腾讯。"

    await generateID.finish(msg0)


rollD = on_command("/roll", rule=check_banlist())


@rollD.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
    args = str(event.message).strip()

    if args:
        state['resu'] = args


@rollD.got("resu", prompt="roll 参数不能为空~！\ndemo：1d10 或 2d10+2d10")
async def _(bot: Bot, event: Event, state: dict) -> None:
    resu = state['resu']
    match = re.match(r'^([\dd+\s]+?)$', resu)

    if not match:
        await rollD.finish("请输入正确的参数！！\ndemo：1d10 或 2d10+2d10")

    await rollD.finish(Roll().roll_dice(resu))


plugin_name_1 = 'genshin-search'
genshinInfo = on_command('/genshin',
                         rule=check_banlist()
                         & check_switch(plugin_name_1, True))


@genshinInfo.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
    args = str(event.message).strip()

    if args:
        state['uid'] = args


@genshinInfo.got('uid', prompt='请告诉咱需要查询的UID，暂时只支持国服嗷~（')
async def _(bot: Bot, event: Event, state: dict) -> None:
    uid = str(state['uid'])

    if (len(uid) == 9):
        await bot.send(event, '别急，在搜索了！')
        uid_info = ''

        try:
            uid_info = Genshin().JsonAnalysis(Genshin().GetInfo(uid))
        except:
            await genshinInfo.finish(
                errorRepo("数据请求错误，原因可能为ID输入错误或不存在\n暂时只支持国服查询（"))

        msg0 = f'{uid} Genshin Info:\n'
        msg0 += uid_info
        print(uid_info)
        await genshinInfo.finish(msg0)

    else:
        await genshinInfo.finish('UID检查未通过，请确保此ID为9位数或者是否为国服ID~！')
