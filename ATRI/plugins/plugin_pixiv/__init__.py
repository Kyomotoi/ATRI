#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2020/11/07 14:31:30
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2020 Kyomotoi, All Rights Reserved.
'''
__author__ = 'kyomotoi'

import re
import json
from requests import exceptions

from nonebot.plugin import on_command
from nonebot.typing import Bot, Event

from ATRI.utils.utils_error import errorRepo
from ATRI.utils.utils_img import aio_download_pics
from ATRI.utils.utils_rule import check_banlist, check_switch

plugin_name_0 = "pixiv-pic-search"
pixivSearchIMG = on_command('p站搜图',
                            rule=check_banlist() & check_switch(plugin_name_0, True))


@pixivSearchIMG.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
    user = str(event.user_id)
    group = str(event.group_id)

    state["user"] = user
    state["group"] = group

    pid = str(event.message).strip()

    if pid:
        state["pid"] = pid


@pixivSearchIMG.got("pid", prompt="请发送目标PID码")
async def _(bot: Bot, event: Event, state: dict) -> None:
    pid = state["pid"]
    pid = re.findall(r"\d+", pid)

    if len(pid):
        pass
    else:
        await pixivSearchIMG.reject("请发送纯阿拉伯数字的pid")

    await bot.send(event, "别急！在搜索了！")

    URL = f"https://api.imjad.cn/pixiv/v1/?type=illust&id={pid[0]}"
    data = {}

    try:
        data = json.loads(await aio_download_pics(URL))
    except exceptions:
        await pixivSearchIMG.finish(errorRepo("请求数据失败"))

    IMG = data["response"][0]["image_urls"]["large"]
    IMG = IMG.replace("i.pximg.net", "i.pixiv.cat")

    msg0 = f'[CQ:at,qq={state["user"]}]\n'
    msg0 += "Search result:\n"
    msg0 += f"Pid: {pid[0]}\n"
    msg0 += f'Title {data["response"][0]["title"]}\n'
    msg0 += f'W&H: {data["response"][0]["width"]}x{data["response"][0]["height"]}\n'
    msg0 += f'Tags: {data["response"][0]["tags"]}\n'
    msg0 += f'Account Name: {data["response"][0]["user"]["account"]}\n'
    msg0 += f'Author Name: {data["response"][0]["user"]["name"]}\n'
    msg0 += f'Link: https://www.pixiv.net/users/{data["response"][0]["user"]["id"]}\n'
    msg0 += IMG

    await pixivSearchIMG.finish(msg0)


plugin_name_1 = "pixiv-author-search"
pixivSearchAuthor = on_command("p站画师",
                               rule=check_banlist()
                               & check_switch(plugin_name_1, True))


@pixivSearchAuthor.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
    user = str(event.user_id)
    group = str(event.group_id)

    state["user"] = user
    state["group"] = group

    author_id = str(event.message).strip()

    if author_id:
        state["author_id"] = author_id


@pixivSearchAuthor.got("author_id", prompt="请发送目标画师id")
async def _(bot: Bot, event: Event, state: dict) -> None:
    author_id = state["author_id"]
    author_id = re.findall(r"\d+", author_id)

    if len(author_id):
        pass
    else:
        await pixivSearchAuthor.reject("请发送纯阿拉伯数字的画师id")

    await bot.send(event, f"别急！在搜索了！\n将展示画师[{author_id[0]}]的前三项作品")

    URL = f"https://api.imjad.cn/pixiv/v1/?type=member_illust&id={author_id[0]}"
    data = {}

    try:
        data = json.loads(await aio_download_pics(URL))
    except exceptions:
        await pixivSearchAuthor.finish(errorRepo("请求网络失败"))

    d = {}

    for i in range(0, 3):
        pid = data["response"][i]["id"]
        title = data["response"][i]["title"]
        IMG = data["response"][i]["image_urls"]["large"]
        IMG = IMG.replace("i.pximg.net", "i.pixiv.cat")
        d[i] = [f"{pid}", f"{title}", f"{IMG}"]

    msg = f'[CQ:at,qq={state["user"]}]'

    result = sorted(d.items(), key=lambda x: x[1], reverse=True)

    t = 0

    for i in result:
        t += 1
        msg += "\n————————————\n"
        msg += f"({t})\n"
        msg += f"Title: {i[1][1]}\n"
        msg += f"Pid: {i[1][0]}\n"
        msg += f"{i[1][2]}"

    await pixivSearchAuthor.finish(msg)


plugin_name_2 = "pixiv-rank"
pixivRank = on_command("p站排行榜",
                       rule=check_banlist() & check_switch(plugin_name_2, True))


@pixivRank.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
    user = str(event.user_id)

    await bot.send(event, "正在获取P站每日排行榜前五作品")

    URL = "https://api.imjad.cn/pixiv/v1/?type=rank"
    data = {}

    try:
        data = json.loads(await aio_download_pics(URL))
    except exceptions:
        await pixivRank.finish(errorRepo("网络请求失败"))

    d = {}

    for i in range(0, 5):
        pid = data["response"][0]["works"][i]["work"]["id"]
        title = data["response"][0]["works"][i]["work"]["title"]
        IMG = data["response"][i]["works"]["image_urls"]["large"]
        IMG = IMG.replace("i.pximg.net", "i.pixiv.cat")
        d[i] = [f"{pid}", f"{title}", f"{IMG}"]

    msg = f"[CQ:at,qq={user}]"

    result = sorted(d.items(), key=lambda x: x[1], reverse=True)

    t = 0

    for i in result:
        t += 1
        msg += "\n————————————\n"
        msg += f"({t})\n"
        msg += f"Title: {i[1][1]}"
        msg += f"Pid: {i[1][0]}"
        msg += f"{i[1][2]}"

    await pixivRank.finish(msg)
