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
import asyncio
from pathlib import Path
from random import randint

from nonebot.plugin import on_command
from nonebot.typing import Bot, Event
from nonebot.permission import GROUP_ADMIN, GROUP_OWNER, SUPERUSER

from ATRI.utils.utils_yml import load_yaml
from ATRI.utils.utils_error import errorRepo
from ATRI.utils.utils_rule import check_banlist
from ATRI.utils.utils_textcheck import PUBLIC_OPINION_PATH, Textcheck
from ATRI.utils.utils_switch import controlSwitch

CONFIG_PATH = Path('.') / 'config.yml'
master = load_yaml(CONFIG_PATH)['bot']['superusers']

switch = on_command('switch',
                    rule=check_banlist(),
                    permission=(SUPERUSER | GROUP_OWNER | GROUP_ADMIN))


@switch.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
    user = str(event.user_id)
    group = str(event.group_id)
    func = str(event.message).strip()

    SWITCH_PATH = Path('.') / 'ATRI' / 'utils' / 'utils_rule' / 'switch.json'
    with open(SWITCH_PATH, 'r') as f:
        data = json.load(f)

    if not func:
        msg0 = "-==ATRI Switch Control System==-\n"
        msg0 += "Usage: switch on/off-{service}\n"
        msg0 += "* For SUPERUSER:\n"
        msg0 += "  - Usage: switch all-on/off-{service}\n"
        msg0 += "Service:\n"

        for i in data.keys():
            msg0 += f"    {i}\n"

        await switch.finish(msg0)

    funct = re.findall(r"[on|off]-(.*)", func)

    if "all-on" in func:
        if int(user) in master:
            await switch.finish(controlSwitch(funct[0], True))

        else:
            await switch.finish("Permission Denied")

    elif "all-off" in func:
        if int(user) in master:
            await switch.finish(controlSwitch(funct[0], False))

        else:
            await switch.finish("Permission Denied")

    elif "on" in func:
        await switch.finish(controlSwitch(funct[0], True, group))

    elif "off" in func:
        await switch.finish(controlSwitch(funct[0], False, group))

    else:
        await switch.finish("请检查拼写是否正确嗷~~！")


# 舆情监控系统
publicOpinion = on_command("舆情", rule=check_banlist(), permission=SUPERUSER)


@publicOpinion.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
    msg = str(event.message).strip().split(' ')

    with open(PUBLIC_OPINION_PATH, 'r') as f:
        data = json.load(f)

    if msg[0] == '':
        msg0 = "---=====ATRI POM System=====---\n"
        msg0 += "Usage:\n"
        msg0 += "  - 舆情 [key] [repo] [times] [ban time(bot)]\n"
        msg0 += "  - 舆情 del [key]\n"
        msg0 += "  - 舆情 list\n"
        msg0 += "Tips:\n"
        msg0 += " - 非 SUPERU 只能设置本群\n"
        msg0 += " - SUPERU 需在后跟随 -a 以启用全局效果\n"
        msg0 += " - 参数类型:\n"
        msg0 += "    * key: 关键词(将使用正则匹配)\n"
        msg0 += "    * repo: 触发后的关键词(可选)，如为图片，键入 img\n"
        msg0 += "    * times: 容忍次数(n>0, int)\n"
        msg0 += "    * ban time: bot对其失效时间(min, int)"

        await publicOpinion.finish(msg0)

    if msg[0] == 'del':
        await publicOpinion.finish(Textcheck().del_word(msg[1]))

    if msg[0] == 'list':
        msg0 = "舆情检测列表如下：\n"
        for w in data.keys():
            msg0 += f'   {w}\n'

    if msg[0] and msg[1] and msg[2] and msg[3]:
        pass
    else:
        msg0 = "请检查格式奥~！\n"
        msg0 += "舆情 [key] [repo] [times] [ban time(bot)]\n"
        msg0 += " * key: 关键词(将使用正则匹配)\n"
        msg0 += " * repo: 触发后的关键词(可选)，如为图片，键入 img\n"
        msg0 += " * times: 容忍次数(n>0, int)\n"
        msg0 += " * ban time: bot对其失效时间(min, int)"
        await publicOpinion.finish(msg0)

    key = msg[0]
    repo = msg[1]
    max_times = msg[2]
    ban_time = msg[3]

    if key and repo and max_times and ban_time:
        if not re.findall(r"/^\d{1,}$/", max_times) and re.findall(
                r"/^\d{1,}$/", ban_time):
            await publicOpinion.finish("非法字符！请注意(times, ban time)类型为int(阿拉伯数字)"
                                       )

    else:
        await publicOpinion.finish("请键入完整信息！\n如需帮助，请键入：舆情")

    if repo == "img":
        state["key"] = key
        state["max_times"] = max_times
        state["ban_time"] = ban_time

    else:
        await publicOpinion.finish(Textcheck().add_word(
            key, repo, int(max_times), int(ban_time)))


@publicOpinion.got("repo", prompt="检测到 repo 类型为 img，请发送一张图片")
async def _(bot: Bot, event: Event, state: dict) -> None:
    key = state["key"]
    repo = state["repo"]
    max_times = state["max_times"]
    ban_time = state["ban_time"]

    if "[CQ:image" not in repo:
        await publicOpinion.reject("请发送一张图片而不是图片以外的东西~！（")

    await publicOpinion.finish(Textcheck().add_word(key, repo, int(max_times),
                                                    int(ban_time)))


trackError = on_command("track", permission=SUPERUSER)
file_error = Path('.') / 'ATRI' / 'data' / 'data_Error' / 'error.json'


@trackError.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
    args = str(event.message).strip()

    if args:
        state['track_id'] = args


@trackError.got('track_id', prompt='请告诉咱追踪ID嗷~！不然无法获取错误堆栈呢！！')
async def _(bot: Bot, event: Event, state: dict) -> None:
    track_id = state['track_id']

    data = {}

    try:
        with open(file_error, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        await trackError.finish(errorRepo("读取文件时错误"))

    if track_id in data:
        info_error = data[track_id]

        msg0 = f"trackID: {track_id}\n"
        msg0 = +info_error

        await trackError.finish(msg0)

    else:
        await trackError.finish("未发现该ID")


groupSendMessage = on_command("群发", permission=SUPERUSER)


@groupSendMessage.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
    args = str(event.message).strip()

    if args:
        state['msg'] = args


@groupSendMessage.got('msg', prompt='请告诉咱需要群发的内容~！')
async def _(bot: Bot, event: Event, state: dict) -> None:
    msg = state['msg']
    group_list = await bot.get_group_list()
    sc_list = []
    err_list = []

    with open(Path('.') / 'utils' / 'utils_rule' / 'ban_list_group.json',
              'r') as f:
        ban_group_list = json.load(f)

    for group in group_list:
        if group['group_id'] not in ban_group_list:
            asyncio.sleep(randint(1, 5))
            try:
                await bot.send_group_msg(group_id=group['group_id'],
                                         message=msg)
                sc_list.append(group['group_id'])
            except:
                await bot.send(event, f"在尝试推送到群[{group['group_id']}]时失败了呢...")
                err_list.append(group['group_id'])

    msg0 = ""
    for i in err_list:
        msg0 += f"  {i}\n"

    repo_msg = f"推送信息：\n{msg}"
    repo_msg += "\n————————\n"
    repo_msg += f"总共：{len(group_list)}\n"
    repo_msg += f"成功推送：{len(sc_list)}\n"
    repo_msg += f"失败[{len(err_list)}]个：\n"
    repo_msg += msg0

    await groupSendMessage.finish(repo_msg)
