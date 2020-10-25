#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2020/10/11 14:37:53
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2020 Kyomotoi, All Rights Reserved.
'''
__author__ = 'kyomotoi'

import re
import json
from pathlib import Path

from nonebot.plugin import on_command
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.permission import GROUP_ADMIN, GROUP_OWNER, SUPERUSER

from utils.utils_banList import banList
from utils.utils_switch import controlSwitch

import ATRI


master = ATRI.config_SUPERUSERS


switch = on_command('switch', permission=(SUPERUSER|GROUP_OWNER|GROUP_ADMIN))

@switch.handle() # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
    user = str(event.user_id)
    group = str(event.group_id)

    if banList(user, group):
        func = str(event.message).strip()
        
        if func:
            pass
        else:
            msg0 = "-==ATRI Switch Control System==-\n"
            msg0 += "┌Usage: switch on/off-{service}\n"
            msg0 += "├For SUPERUSER:\n"
            msg0 += "│  └Usage: switch all-on/off-{service}\n"
            msg0 += "└Service:\n"
            msg0 += "    ├anime-setu\n"
            msg0 += "    ├anime-pic-search\n"
            msg0 += "    ├anime-vid-search\n"
            msg0 += "    ├ai-face\n"
            msg0 += "    ├pixiv-pic-search\n"
            msg0 += "    ├pixiv-author-search\n"
            msg0 += "    └pixiv-rank"

            await switch.finish(msg0)
        
        funct = re.findall(r"[on|off]-(.*)", func)
        
        if "all-on" in func:
            if int(user) in master:
                await switch.finish(controlSwitch(funct[0], True))

            else:
                await switch.finish("You don't have enough permissions do THIS!")
        
        elif "all-off" in func:
            if int(user) in master:
                await switch.finish(controlSwitch(funct[0], False))

            else:
                await switch.finish("You don't have enough permissions do THIS!")
        
        elif "on" in func:
            await switch.finish(controlSwitch(funct[0], True, group))
        
        elif "off" in func:
            await switch.finish(controlSwitch(funct[0], False, group))

        else:
            await switch.finish("请检查拼写是否正确嗷~~！")


# # 舆情监控系统
# publicOpinion = on_command("舆情", permission=SUPERUSER|GROUP_ADMIN|GROUP_OWNER)
# data_PO = Path('.') / 'ATRI' / 'plugins' / 'plugin_chat' / 'public_opinion.json'

# @publicOpinion.handle() # type: ignore
# async def _(bot: Bot, event: Event, state: dict) -> None:
#     user = str(event.user_id)
#     group = str(event.group_id)
#     msg = str(event.message).strip().split(' ')

#     if banList(user, group):
#         if msg[0] == '':
#             msg0 = "---=====ATRI POM System=====---\n"
#             msg0 += "Usage:\n"
#             msg0 += "  - 舆情 [key] [times] [ban time(bot)] [repo]\n"
#             msg0 += "Tips:\n"
#             msg0 += " - 非 SUPERU 只能设置本群\n"
#             msg0 += " - SUPERU 需在后跟随 -a 以启用全局效果\n"
#             msg0 += " - 参数类型:\n"
#             msg0 += "    * key: 关键词(将使用正则匹配)\n"
#             msg0 += "    * times: 容忍次数(n>0, int)\n"
#             msg0 += "    * ban time: bot对其失效时间(min, int)\n"
#             msg0 += "    * repo: 触发后的关键词(可选)，如为图片，键入 img"

#             await publicOpinion.finish(msg0)
        
#         key_word = msg[0]
#         remind = msg[1]
#         punish = msg[2]
#         repo = msg[3]

#         if key_word and remind and punish and repo:
#             if re.findall(r"/^\d{1,}$/", remind) and re.findall(r"/^\d{1,}$/", punish):
#                 pass

#             else:
#                 await publicOpinion.finish("非法字符！请注意(times, ban time)类型为int(阿拉伯数字)")
        
#         else:
#             await publicOpinion.finish("请键入完整信息！\n如需帮助，请键入 舆情")
        
#         if repo == "img":
#             state["key_word"] = key_word
#             state["remind"] = remind
#             state["punish"] = punish
        
#         else:
#             pass

# @publicOpinion.got("repo", prompt="检测到 repo 类型为 img，请发送一张图片") # type: ignore
# async def _(bot: Bot, event: Event, state: dict) -> None:
#     key_word = state["key_word"]
#     remind = state["remind"]
#     punish = state["punish"]
#     repo = state["repo"]

#     if "[CQ:image" not in repo:
#         await publicOpinion.reject("请发送一张图片而不是图片以外的东西~！（")
    
#     try:
#         with open(data_PO, "r") as f:
#             data = json.load(f)
#     except:
#         data = {}

#     data[key_word] = [remind, punish, repo]
