#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2020/10/11 14:38:38
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2020 Kyomotoi, All Rights Reserved.
'''
__author__ = 'kyomotoi'

from random import choice

from nonebot.log import logger
from nonebot.permission import GROUP_ADMIN, GROUP_OWNER, SUPERUSER
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.plugin import on_command, on_message, on_notice

from utils.utils_banList import banList
from utils.utils_history import saveMessage


# 收集 bot 所在群的聊天记录
MessageSave = on_message()

@MessageSave.handle() # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
    user = str(event.user_id)
    group = str(event.group_id)
    message = str(event.message)
    message_id = str(event.id)

    if group == "None":
        saveMessage(message_id, message, user)
    else:
        saveMessage(message_id, message, user, group)
    
    logger.opt(colors=True).info(f"[<yellow>{group}</yellow>]-U: (<blue>{user}</blue>) | Message: (<green>{message}</green>) Saved successfully")


# Call bot
callMe = on_message()

@callMe.handle() # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
    user = str(event.user_id)
    group = str(event.group_id)

    if banList(user, group):
        msg = str(event.message)

        if "ATRI" == msg or "亚托莉" == msg or "アトリ" == msg:
            await callMe.finish("叫我有啥事吗w")
        
        elif "萝卜子" in msg:
            await bot.send(event, "萝卜子是对咱的蔑称！！")
        
        else:
            pass


# 戳 一 戳
pokehah = on_command("戳一戳", rule=to_me())

@pokehah.handle() # type: ignore
async def _poke(bot: Bot, event: Event, state: dict) -> None:
    user = str(event.user_id)
    group = str(event.group_id)

    if banList(user, group):
        msg = choice(
                    [
                        "你再戳！",
                        "？再戳试试？",
                        "别戳了别戳了再戳就坏了555",
                        "我爪巴爪巴，球球别再戳了",
                        "你戳你🐎呢？！",
                        "那...那里...那里不能戳...绝对...",
                        "(。´・ω・)ん?",
                        "有事恁叫我，别天天一个劲戳戳戳！",
                        "欸很烦欸！你戳🔨呢",
                        "?"
                    ])

        await pokehah.finish(msg)


async def poke_(bot: Bot, event: Event, state: dict) -> bool:
    return (event.detail_type == "notify" and event.raw_event["sub_type"] == "poke" and
            event.sub_type == "notice" and int(event.self_id) == event.raw_event["target_id"])

poke = on_notice(poke_, block=True)
poke.handle()(_poke)


# 处理进 / 退 裙事件
groupEvent = on_notice()

@groupEvent.handle() # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
    group = str(event.group_id)
    print(event.raw_event)

    if banList(group):
        if event.raw_event["notice_type"] == "group_increase":
            await groupEvent.finish(f'好欸！事新人[CQ:at,qq={event.raw_event["user_id"]}]')
            await groupEvent.finish(f"在下 ATRI，你可以叫我 亚托莉 或 アトリ ！~w")

        elif event.raw_event["notice_type"] == "group_decrease":
            await groupEvent.finish(f'[{event.raw_event["operator_id"]}] 离开了我们...')


# 舆情监听系统