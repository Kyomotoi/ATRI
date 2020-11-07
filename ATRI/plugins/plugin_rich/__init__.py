#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2020/10/11 14:40:34
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2020 Kyomotoi, All Rights Reserved.
'''
__author__ = 'kyomotoi'

import re
import json
import requests

from nonebot.log import logger
from nonebot.plugin import on_message
from nonebot.adapters.cqhttp import Bot, Event

from utils.utils_times import countX
from utils.utils_rule import check_banlist
from utils.utils_request import request_get
from .body import dec

BILI_REPORT_FORMAT = """[{aid}] Info:
Title: {title}
bid: {bid}
Viev: {view} Like: {like}
Coin: {coin} Share: {share}
Link:
{aid_link}
{bid_link}"""

bilibiliRich = on_message(rule=check_banlist())
b_list = []


@bilibiliRich.handle()  # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
    global b_list
    user = event.user_id
    msg = str(event.message)

    # 防刷屏机制：回复次数达到五次自动忽略下一次
    if countX(b_list, user) == 5:
        return

    if "qqdocurl" not in msg:
        try:
            bv = re.findall(r"(BV\w+)", msg)
        except:
            return
    else:
        bvURL = re.findall(r"(........b23...\S+\=)", msg)

        try:
            r = requests.get(bvURL[0], stream=True, allow_redirects=True)
        except:
            logger.waring("Get BV ERROR. (Request ERROR)")
            return

        bv = re.findall(r"(BV\w+)", r.url)

    if bv:
        aid = str(dec(bv[0]))
        ad = 'av' + aid
        URL = f'https://api.imjad.cn/bilibili/v2/?aid={aid}'

        try:
            res = request_get(URL)
        except:
            logger.waring("Request ERROR")
            return

        data = json.loads(res)
        msg = BILI_REPORT_FORMAT.format(title=data["data"]["title"],
                                        view=data["data"]["stat"]["view"],
                                        coin=data["data"]["stat"]["coin"],
                                        share=data["data"]["stat"]["share"],
                                        like=data["data"]["stat"]["like"],
                                        bid=data["data"]["bvid"],
                                        bid_link=data["data"]["short_link"],
                                        aid=ad,
                                        aid_link=f'https://b23.tv/{ad}')

        b_list.append(user)
        await bilibiliRich.finish(msg)

    else:
        return


CLOUDMUSIC_REPORT_FORMAT = """Status: {status}
Song id: {id}
Br: {br}
Download: {url}
MD5: {md5}"""

cloudmusicRich = on_message(rule=check_banlist())
c_list = []


@cloudmusicRich.handle()  # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
    global c_list
    user = event.user_id
    msg = str(event.message)

    # 防刷屏机制：回复次数达到五次自动忽略下一次
    if countX(b_list, user) == 5:
        return

    if "music.163.com" in msg:
        music_id = re.findall(r"song\S+\/|id=\S+\&", msg)

        if music_id:
            music_id = str(music_id[0])
            music_id = re.findall(r"-?[1-9]\d*", music_id)
            URL = f'https://api.imjad.cn/cloudmusic/?type=song&id={music_id[0]}&br=320000'

            try:
                res = request_get(URL)
            except:
                logger.waring("Request ERROR")
                return

            data = json.loads(res)
            msg = CLOUDMUSIC_REPORT_FORMAT.format(
                status=data["code"],
                id=data["data"][0]["id"],
                br=data["data"][0]["br"],
                url=data["data"][0]["url"],
                md5=data["data"][0]["md5"],
            )

            c_list.append(user)
            await cloudmusicRich.finish(msg)

    else:
        return
