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
from utils.utils_error import errorRepo

from nonebot.plugin import on_command
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.permission import GROUP_ADMIN, GROUP_OWNER, SUPERUSER

from utils.utils_yml import load_yaml
from utils.utils_rule import check_banlist
from utils.utils_switch import controlSwitch

CONFIG_PATH = Path('.') / 'config.yml'
master = load_yaml(CONFIG_PATH)['bot']['superusers']

switch = on_command('switch',
                    rule=check_banlist(),
                    permission=(SUPERUSER | GROUP_OWNER | GROUP_ADMIN))


@switch.handle()  # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
    user = str(event.user_id)
    group = str(event.group_id)

    func = str(event.message).strip()

    if not func:
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
publicOpinion = on_command("舆情",
                           rule=check_banlist(),
                           permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)
data_PO = Path(
    '.') / 'ATRI' / 'plugins' / 'plugin_chat' / 'public_opinion.json'


@publicOpinion.handle()  # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
    msg = str(event.message).strip().split(' ')

    if msg[0] == '':
        msg0 = "---=====ATRI POM System=====---\n"
        msg0 += "Usage:\n"
        msg0 += "  - 舆情 [key] [times] [ban time(bot)] [repo]\n"
        msg0 += "Tips:\n"
        msg0 += " - 非 SUPERU 只能设置本群\n"
        msg0 += " - SUPERU 需在后跟随 -a 以启用全局效果\n"
        msg0 += " - 参数类型:\n"
        msg0 += "    * key: 关键词(将使用正则匹配)\n"
        msg0 += "    * times: 容忍次数(n>0, int)\n"
        msg0 += "    * ban time: bot对其失效时间(min, int)\n"
        msg0 += "    * repo: 触发后的关键词(可选)，如为图片，键入 img"

        await publicOpinion.finish(msg0)

    if msg[0] and msg[1] and msg[2] and msg[3]:
        pass
    else:
        msg0 = "请检查格式奥~！\n"
        msg0 += "舆情 [key] [times] [ban time(bot)] [repo]\n"
        msg0 += " * key: 关键词(将使用正则匹配)\n"
        msg0 += " * times: 容忍次数(n>0, int)\n"
        msg0 += " * ban time: bot对其失效时间(min, int)\n"
        msg0 += " * repo: 触发后的关键词(可选)，如为图片，键入 img"
        await publicOpinion.finish(msg0)

    key_word = msg[0]
    remind = msg[1]
    punish = msg[2]
    repo = msg[3]

    if key_word and remind and punish and repo:
        if re.findall(r"/^\d{1,}$/", remind) and re.findall(
                r"/^\d{1,}$/", punish):
            pass

        else:
            await publicOpinion.finish("非法字符！请注意(times, ban time)类型为int(阿拉伯数字)"
                                       )

    else:
        await publicOpinion.finish("请键入完整信息！\n如需帮助，请键入 舆情")

    if repo == "img":
        state["key_word"] = key_word
        state["remind"] = remind
        state["punish"] = punish

    else:
        try:
            with open(data_PO, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        data[key_word] = [remind, punish, repo]

        with open(data_PO, "w") as f:
            f.write(json.dumps(data))
            f.close()

        msg0 = "舆情信息记录完成~！\n"
        msg0 += f"Keyword: {key_word}\n"
        msg0 += f"Times: {remind}\n"
        msg0 += f"Ban time: {punish}\n"
        msg0 += f"Repo: {repo}"

        await publicOpinion.finish(msg0)


@publicOpinion.got("repo", prompt="检测到 repo 类型为 img，请发送一张图片")  # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
    key_word = state["key_word"]
    remind = state["remind"]
    punish = state["punish"]
    repo = state["repo"]

    if "[CQ:image" not in repo:
        await publicOpinion.reject("请发送一张图片而不是图片以外的东西~！（")

    try:
        with open(data_PO, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    data[key_word] = [remind, punish, repo]

    with open(data_PO, "w") as f:
        f.write(json.dumps(data))
        f.close()

    msg0 = "舆情信息记录完成~！\n"
    msg0 += f"Keyword: {key_word}\n"
    msg0 += f"Times: {remind}\n"
    msg0 += f"Ban time: {punish}\n"
    msg0 += f"Repo: {repo}"

    await publicOpinion.finish(msg0)


trackError = on_command("track", permission=SUPERUSER)
file_error = Path('.') / 'ATRI' / 'data' / 'data_Error' / 'error.json'


@trackError.handle()  # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
    track_id = str(event.message).strip()

    if not track_id:
        await trackError.finish("请告诉咱追踪ID嗷~！不然无法获取错误堆栈呢！！")

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


@groupSendMessage.handle()  # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
    args = str(event.message).strip()

    if args:
        state['msg'] = args


@groupSendMessage.got('msg', prompt='请告诉咱需要群发的内容~！')  # type: ignore
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
