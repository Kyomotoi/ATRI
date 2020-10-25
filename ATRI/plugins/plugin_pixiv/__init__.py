#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2020/10/11 14:38:49
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2020 Kyomotoi, All Rights Reserved.
'''
__author__ = 'kyomotoi'

import re
import json

from nonebot.plugin import on_command
from nonebot.adapters.cqhttp import Bot, Event

from utils.utils_error import errorRepo
from utils.utils_banList import banList
from utils.utils_switch import checkSwitch
from utils.utils_request import request_get


plugin_name_0 = "pixiv-pic-search"
pixivSearchIMG = on_command('p站搜图')

@pixivSearchIMG.handle() # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
    user = str(event.user_id)
    group = str(event.group_id)

    state["user"] = user
    state["group"] = group

    if banList(user, group):
        if checkSwitch(plugin_name_0, group):
            pid = str(event.message).strip()

            if pid:
                state["pid"] = pid
        else:
            await pixivSearchIMG.finish(f"Service-{plugin_name_0} has been closed.")

@pixivSearchIMG.got("pid", prompt="请发送目标PID码") # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
    pid = state["pid"]
    pid = re.findall(r"\d+", pid)

    if len(pid):
        pass
    else:
        await pixivSearchIMG.reject("请发送纯阿拉伯数字的pid")

    await bot.send(event, "别急！在搜索了！")

    URL = f"https://api.imjad.cn/pixiv/v1/?type=illust&id={pid}"
    data = {}

    try:
        data = json.loads(request_get(URL))
    except:
        await pixivSearchIMG.finish(errorRepo("请求数据失败"))
    
    msg0 = f'[CQ:at,qq={state["user"]}]\n'
    msg0 += f"Search result:\n"
    msg0 += f"Pid: {pid}\n"
    msg0 += f'Title {data["response"][0]["title"]}\n'
    msg0 += f'W&H: {data["response"][0]["width"]}x{data["response"][0]["height"]}\n'
    msg0 += f'Tags: {data["response"][0]["tags"]}\n'
    msg0 += f'Account Name: {data["response"][0]["user"]["account"]}\n'
    msg0 += f'Author Name: {data["response"][0]["user"]["name"]}\n'
    msg0 += f'Link: https://www.pixiv.net/users/{data["response"][0]["user"]["id"]}\n'
    msg0 += f'IMG: https://pixiv.cat/{pid}.jpg'

    await pixivSearchIMG.finish(msg0)


plugin_name_1 = "pixiv-author-search"
pixivSearchAuthor = on_command("p站画师")

@pixivSearchAuthor.handle() # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
    user = str(event.user_id)
    group = str(event.group_id)

    state["user"] = user
    state["group"] = group

    if banList(user, group):
        if checkSwitch(plugin_name_1, group):
            author_id = str(event.message).strip()

            if author_id:
                state["author_id"] = author_id
        else:
            await pixivSearchAuthor.finish(f"Service-{plugin_name_1} has been closed.")

@pixivSearchAuthor.got("author_id", prompt="请发送目标画师id") # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
    author_id = state["author_id"]
    author_id = re.findall(r"\d+", author_id)

    if len(author_id):
        pass
    else:
        await pixivSearchAuthor.reject("请发送纯阿拉伯数字的画师id")
    
    await bot.send(event, f"别急！在搜索了！\n将展示画师[{author_id}]的前三项作品")

    URL = f"https://api.imjad.cn/pixiv/v1/?type=member_illust&id={author_id}"
    data = {}

    try:
        data = json.loads(request_get(URL))
    except:
        await pixivSearchAuthor.finish(errorRepo("请求网络失败"))

    for i in range(0,3):
        pid = data["response"][i]["id"]
        IMG = f"https://pixiv.cat/{author_id}.jpg"
        data[i] = [f"{pid}", f"{IMG}"]
    
    msg0 = f'[CQ:at,qq={state["user"]}]\n'
    
    result = sorted(
        data.items(),
        key=lambda x:x[1],
        reverse=True
    )

    t = 0

    for i in result:
        t += 1
        msg = f"\n---------------\n"
        msg += f"({t})\n"
        msg += f"Pid: {i[1][0]}\n{i[1][1]}"
        msg0 += msg
    
    await pixivSearchAuthor.finish(msg0)


plugin_name_2 = "pixiv_rank"
pixivRank = on_command("p站排行榜")

@pixivRank.handle() # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
    user = str(event.user_id)
    group = str(event.group_id)

    if banList(user, group):
        if checkSwitch(plugin_name_2, group):

            await bot.send(event, "正在获取P站每日排行榜前五作品")

            URL = "https://api.imjad.cn/pixiv/v1/?type=rank"
            data = {}

            try:
                data = json.loads(request_get(URL))
            except:
                await pixivRank.finish(errorRepo("网络请求失败"))
            
            for i in range(0,5):
                pid = data["response"][0]["works"][i]["work"]["id"]
                IMG = f"https://pixiv.cat/{pid}.jpg"
                data[i] = [f"{pid}", f"{IMG}"]
            
            msg0 = f"[CQ:at,qq={user}]"

            result = sorted(
                data.items(),
                key=lambda x:x[1],
                reverse=True
            )

            t = 0

            for i in result:
                t += 1
                msg = "\n---------------\n"
                msg += f"({t})\n"
                msg += f"Pid: {i[1][0]}"
                msg += f"{i[1][1]}"
                msg0 += msg
            
            await pixivRank.finish(msg0)
        
        else:
            await pixivRank.finish(f"Service-{plugin_name_2} has been closed.")