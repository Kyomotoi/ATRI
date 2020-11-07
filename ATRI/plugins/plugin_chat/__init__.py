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

import json
from pathlib import Path
from random import choice

from nonebot.log import logger
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.plugin import on_command, on_message, on_notice

from utils.utils_times import countX
from utils.utils_yml import load_yaml
from utils.utils_error import errorRepo
from utils.utils_rule import check_banlist
from utils.utils_history import saveMessage
from utils.utils_request import request_api_text

CONFIG_PATH = Path('.') / 'config.yml'
config = load_yaml(CONFIG_PATH)['bot']

# 收集 bot 所在群的聊天记录
MessageSave = on_message()


@MessageSave.handle()  # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
    user = str(event.user_id)
    group = str(event.group_id)
    message = str(event.message)
    message_id = str(event.id)

    if group == "None":
        saveMessage(message_id, message, user)
    else:
        saveMessage(message_id, message, user, group)

    logger.opt(colors=True).info(
        f"[<yellow>{group}</yellow>]-U: (<blue>{user}</blue>) | Message: (<green>{message}</green>) Saved successfully"
    )


# Call bot
callMe = on_message(rule=check_banlist())


@callMe.handle()  # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
    msg = str(event.message)

    if msg in config['nickname']:
        await callMe.finish("叫咱有啥事吗w")

    elif "萝卜子" in msg:
        await bot.send(event, "萝卜子是对咱的蔑称！！")

    else:
        pass


# 戳 一 戳
pokehah = on_command("戳一戳", rule=to_me() & check_banlist())


@pokehah.handle()  # type: ignore
async def _poke(bot: Bot, event: Event, state: dict) -> None:
    msg = choice([
        "你再戳！", "？再戳试试？", "别戳了别戳了再戳就坏了555", "我爪巴爪巴，球球别再戳了", "你戳你🐎呢？！",
        "那...那里...那里不能戳...绝对...", "(。´・ω・)ん?", "有事恁叫我，别天天一个劲戳戳戳！", "欸很烦欸！你戳🔨呢",
        "?"
    ])

    await pokehah.finish(msg)


async def poke_(bot: Bot, event: Event, state: dict) -> bool:
    return (event.detail_type == "notify"
            and event.raw_event["sub_type"] == "poke"  # type: ignore
            and event.sub_type == "notice" and int(
                event.self_id) == event.raw_event["target_id"]  # type: ignore
            )


poke = on_notice(poke_, block=True)
poke.handle()(_poke)

# 处理 进 / 退 群事件
groupEvent = on_notice(rule=check_banlist())


@groupEvent.handle()  # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
    if event.raw_event["notice_type"] == "group_increase":  # type: ignore
        await groupEvent.finish(
            f'好欸！事新人[CQ:at,qq={event.raw_event["user_id"]}]'  # type: ignore
        )  # type: ignore
        await groupEvent.finish(f"在下 ATRI，你可以叫我 亚托莉 或 アトリ ！~w")

    elif event.raw_event[  # type: ignore
            "notice_type"] == "group_decrease":
        await groupEvent.finish(
            f'[{event.raw_event["operator_id"]}] 离开了我们...'  # type: ignore
        )


# 舆情监听系统
listenPublicOpinion = on_message()
file_PO = Path(
    '.') / 'ATRI' / 'plugins' / 'plugin_chat' / 'public_opinion.json'


@groupEvent.handle()  # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
    with open(file_PO, 'r') as f:
        data = json.load(f)


# 口臭一下
fxxkMe = on_command('口臭一下',
                    aliases={'口臭', '骂我'},
                    rule=to_me() & check_banlist())
list_M = []


@fxxkMe.handle()  # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
    user = str(event.user_id)
    global list_M

    if countX(list_M, user) >= 3:
        await fxxkMe.finish("不是？？你这么想被咱骂的嘛？？被咱骂就这么舒服的吗？！该......你该不会是.....M吧！")

    elif countX(list_M, user) >= 6:
        await fxxkMe.finish("给我适可而止阿！？")
        list_M = list(set(list_M))

    else:
        list_M.append(user)
        URL = "https://nmsl.shadiao.app/api.php?level=min&lang=zh_cn"
        msg = ""

        try:
            msg = request_api_text(URL)
        except:
            await fxxkMe.finish(errorRepo("请求错误"))

        await fxxkMe.finish(msg)


# Hitokoto
hitokoto = on_command('一言',
                      aliases={'抑郁一下', '网抑云'},
                      rule=to_me() & check_banlist())
list_Y = []


@hitokoto.handle()  # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
    user = str(event.user_id)
    global list_Y

    if countX(list_Y, user) >= 3:
        await hitokoto.finish("额......需要咱安慰一下嘛~？")

    elif countX(list_Y, user) >= 6:
        await hitokoto.finish("如果心里感到难受就赶快去睡觉奥！别再憋自己了！")
        list_Y = list(set(list_Y))

    else:
        list_Y.append(user)
        URL = "https://api.imjad.cn/hitokoto/?cat=a&charset=utf-8&length=50&encode=json&fun=sync&source="
        info = {}

        try:
            info = json.loads(request_api_text(URL))
        except:
            await hitokoto.finish(errorRepo("请求错误"))

        await hitokoto.finish(info["hitokoto"])
