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
from random import choice, randint, sample

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

switch = on_command('/switch',
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
        msg0 += "Usage: /switch on/off-{service}\n"
        msg0 += "* For SUPERUSER:\n"
        msg0 += "  - Usage: /switch all-on/off-{service}\n"
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
# Usage:
#   - /pubopin [key] [repo] [times] [ban time(bot)]
#   - /pubopin del [key]
#   - /pubopin list
# Tips:
#  - 参数类型:
#     * key: 关键词(将使用正则匹配)
#     * repo: 触发后的关键词(可选)，如为图片，键入 img
#     * times: 容忍次数(n>0, int)
#     * ban time: bot对其失效时间(min, int)
publicOpinion = on_command("/pubopin",
                           rule=check_banlist(),
                           permission=SUPERUSER)


@publicOpinion.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
    msg = str(event.message).strip().split(' ')

    with open(PUBLIC_OPINION_PATH, 'r') as f:
        data = json.load(f)

    if msg[0] == '':
        await publicOpinion.finish("请查看文档获取帮助（")

    if msg[0] == 'del':
        await publicOpinion.finish(Textcheck().del_word(msg[1]))

    if msg[0] == 'list':
        msg0 = "舆情检测列表如下：\n"
        for w in data.keys():
            msg0 += f'   {w}\n'

    if not msg[0] or not msg[1] or not msg[2] or not msg[3]:
        await publicOpinion.finish("ごんめなさい...请检查格式嗷...")

    if not re.findall(r"/^\d{1,}$/", msg[2]) or not re.findall(
            r"/^\d{1,}$/", msg[3]):
        await publicOpinion.finish("非法字符！咱不接受除int以外的类型！！")

    if msg[1] == "img":
        state["key"] = msg[0]
        state["max_times"] = msg[2]
        state["ban_time"] = msg[3]

    else:
        await publicOpinion.finish(Textcheck().add_word(
            msg[0], msg[1], int(msg[2]), int(msg[3])))


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


trackError = on_command("/track", permission=SUPERUSER)
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


groupSendMessage = on_command("/groupsend", permission=SUPERUSER)


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


# keyRepoAddReview = on_command('关键词审核', permission=SUPERUSER)
# KEY_PATH = Path('.') / 'ATRI' / 'plugins' / 'plugin_chat' / 'key_repo.json'
# KEY_WAITING_PATH = Path(
#     '.') / 'ATRI' / 'plugins' / 'plugin_admin' / 'key_repo_waiting.json'
# with open(KEY_PATH, 'r', encoding='utf-8') as f:
#     data = json.load(f)
# with open(KEY_WAITING_PATH, 'r', encoding='utf-8') as f:
#     data_rev = json.load(f)


# @keyRepoAddReview.got('rev')
# @keyRepoAddReview.args_parser
# async def _(bot: Bot, event: Event, state: dict) -> None:
#     rev = state['rev']
#     key = sample(data_rev.keys(), 1)
#     await bot.send(
#         event,
#         f'Key: {data_rev[key]}\nRepo: {data_rev[key][0]}\nProba: {data_rev[key][1]}\nSender: {data_rev[key][2]}\nGroup: {data_rev[key][3]}\nTime: {data_rev[key][4]}'
#     )

#     if rev == '歇了':
#         await keyRepoAddReview.finish("むー……ご苦労様でしたよ。")
#     else:
#         if rev == '通过' or rev == '过' or rev == '好' or rev == 'y':
#             await bot.send(event, '好！')
#             data[data_rev[key]] = [
#                 data_rev[key][0], data_rev[key][1], data_rev[key][2],
#                 data_rev[key][3], data_rev[key][4]
#             ]
#             with open(KEY_PATH, 'w') as f:
#                 f.write(data)
#         elif rev == '不行' or rev == '不' or rev == 'n':
#             del data_rev[key]
#             await bot.send(event, '好8')
