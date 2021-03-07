#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
File: __init__.py
Created Date: 2021-02-07 09:34:23
Author: Kyomotoi
Email: Kyomotoiowo@gmail.com
License: GPLv3
Project: https://github.com/Kyomotoi/ATRI
--------
Last Modified: Sunday, 7th March 2021 3:14:28 pm
Modified By: Kyomotoi (kyomotoiowo@gmail.com)
--------
Copyright (c) 2021 Kyomotoi
'''

import re
import json
from aiohttp.client import ClientSession

from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.plugin import on_message

from ATRI.utils.request import get_bytes
from ATRI.utils.list import count_list, del_list_aim
from ATRI.rule import (
    is_in_banlist,
    is_in_dormant,
)

from .data_source import dec


waiting_list = []


bilibili_rich = on_message(
    rule=is_in_banlist() & is_in_dormant()
)

@bilibili_rich.handle()
async def _bilibili_rich(bot: Bot, event: MessageEvent) -> None:
    global waiting_list
    msg = str(event.raw_message).replace("\\", "")
    user = event.user_id
    bv = False
    
    if count_list(waiting_list, user) == 5:
        waiting_list = del_list_aim(waiting_list, user)
        return

    waiting_list.append(user)
    
    if "qqdocurl" not in msg:
        if "av" in msg:
            av = re.findall(r"(av\d+)", msg)[0].replace('av', '')
        else:
            try:
                bv = re.findall(r"(BV\w+)", msg)
                av = str(dec(bv[0]))
            except:
                return
    else:
        patt = r"(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+"
        bv_url = re.findall(patt, msg)
        bv_url = bv_url[3]
        async with ClientSession() as session:
            async with session.get(
                url=bv_url) as r:
                bv = re.findall(r"(BV\w+)", str(r.url))
                av = dec(bv[0])
    
    if not bv:
        if "av" in msg:
            av = re.findall(r"(av\d+)", msg)[0].replace('av', '')
        else:
            return
    
    try:
        URL = f"https://api.kyomotoi.moe/api/bilibili/v2/?aid={av}"
    except:
        return
    data = json.loads(await get_bytes(URL))['data']
    repo = (
        f"{av} INFO:\n"
        f"Title: {data['title']}\n"
        f"Bid: {data['bvid']}\n"
        f"View: {data['stat']['view']} Like: {data['stat']['like']}\n"
        f"Coin: {data['stat']['coin']} Share: {data['stat']['share']}\n"
        f"Link: {data['short_link']}\n"
        "にまねげぴのTencent rich!"
    )
    await bilibili_rich.finish(repo)
