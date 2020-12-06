#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2020/11/07 14:36:53
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2020 Kyomotoi, All Rights Reserved.
'''
__author__ = 'kyomotoi'

import re
import json
import sqlite3
from pathlib import Path
from random import randint
from datetime import datetime, timedelta
from apscheduler.triggers.date import DateTrigger

from nonebot.rule import Rule
from nonebot.log import logger
from nonebot.typing import Bot, Event
from nonebot.permission import SUPERUSER
from nonebot_plugin_apscheduler import scheduler
from nonebot.plugin import on_message, on_command, on_regex

from ATRI.utils.utils_times import countX
from ATRI.utils.utils_yml import load_yaml
from ATRI.utils.utils_error import errorRepo
from ATRI.utils.utils_history import getMessage
from ATRI.utils.utils_translate import toSimpleString
from ATRI.utils.utils_rule import check_banlist, check_switch
from ATRI.utils.utils_request import aio_get_bytes, request_get
from ATRI.utils.utils_img import compress_image, aio_download_pics

from .data_source import resultRepo

CONFIG_PATH = Path('.') / 'config.yml'
config = load_yaml(CONFIG_PATH)

plugin_name_0 = "anime-pic-search"
key_SauceNAO = config['api']['SauceNaoKEY']

SaucenaoSearch = on_command('以图搜图',
                            rule=check_banlist()
                            & check_switch(plugin_name_0, True))


@SaucenaoSearch.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
    user = str(event.user_id)
    group = str(event.group_id)

    state["user"] = user
    state["group"] = group

    img = str(event.message).strip()

    if img:
        state["img_url"] = img


@SaucenaoSearch.got("img_url", prompt="请发送一张目标图片")
async def _(bot: Bot, event: Event, state: dict) -> None:
    img = state["img_url"]
    img = re.findall(r"(http://.*?)]", img)

    if len(img):
        pass
    else:
        await SaucenaoSearch.reject("请发送一张目标图片，而非文字或其他非图片成分( -'`-; )")

    await bot.send(event, "别急！正在找图！")

    await SaucenaoSearch.finish(resultRepo(state['user'], key_SauceNAO,
                                           img[0]))


SaucenaoSearch_repo = on_message(rule=check_banlist()
                                 & check_switch(plugin_name_0, True))


@SaucenaoSearch_repo.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
    group = str(event.group_id)
    msg = str(event.message)

    if "[CQ:reply" in msg:
        if "搜图" in msg or "识图" in msg:
            if group == "None":
                await SaucenaoSearch_repo.finish("ごめんなさい...\n该功能只对群聊开放哦~~")

            try:
                repo_info = re.findall(r"CQ:reply,id=([0-9]\S+)]", msg)
                msg_id = repo_info[0]
            except Exception:
                logger.error("Get message_id ERROR!")
                await SaucenaoSearch_repo.finish(errorRepo('定位消息内容失败'))
                return

            aim = getMessage(msg_id)[f"{msg_id}"]["message"]
            img = img = re.findall(r"(http://.*?)]", aim)

            if len(img):
                pass
            else:
                await SaucenaoSearch_repo.finish('这消息内貌似没图片呢...')

            await bot.send(event, "别急！正在找图！")

            await SaucenaoSearch.finish(
                resultRepo(state['user'], key_SauceNAO, img[0]))


plugin_name_1 = "anime-vid-search"
AnimeSearch = on_command('以图搜番',
                         rule=check_banlist()
                         & check_switch(plugin_name_1, True))


@AnimeSearch.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
    user = str(event.user_id)
    group = str(event.group_id)

    state["user"] = user
    state["group"] = group

    img = str(event.message).strip()

    if img:
        state["img_url"] = img


@AnimeSearch.got("img_url", prompt="请发送一张目标图片")
async def _(bot: Bot, event: Event, state: dict) -> None:
    img = state["img_url"]
    img = re.findall(r"(http://.*?)]", img)

    if len(img):
        pass
    else:
        await SaucenaoSearch.reject("请发送一张目标图片，而非文字或其他非图片成分（")

    await bot.send(event, "别急！正在搜索！")
    req = None

    URL = f'https://trace.moe/api/search?url={img[0]}'
    try:
        req = await aio_get_bytes(URL)
    except:
        await AnimeSearch.finish(errorRepo("请求数据失败"))

    d = {}
    data = json.loads(req.decode())

    try:
        for i in range(len(data['docs'])):
            if data['docs'][i]['title_chinese'] in d:
                d[data['docs'][i]
                  ['title_chinese']][0] += data['docs'][i]['similarity']

            else:
                m = data['docs'][i]['at'] / 60
                s = data['docs'][i]['at'] % 60

                if data['docs'][i]['episode'] == '':
                    n = 1

                else:
                    n = data['docs'][i]['episode']

                d[toSimpleString(data['docs'][i]['title_chinese'])] = [
                    data['docs'][i]['similarity'], f'第{n}集',
                    f'{int(m)}分{int(s)}秒处'
                ]
    except:
        await AnimeSearch.finish(errorRepo("处理数据失败"))

    result = sorted(
        d.items(),
        key=lambda x: x[1],
        reverse=True)

    t = 0
    msg0 = f'[CQ:at,qq={state["user"]}]\n根据所提供的图片按照相似度找到{len(d)}个结果:'

    for i in result:
        t += 1
        lk = ('%.2f%%' % (i[1][0] * 100))
        msg = (
            f'\n——————————\n({t})\n相似度：{lk}\n动漫名：《{i[0]}》\n时间点：{i[1][1]} {i[1][2]}'
        )
        msg0 += msg

    await AnimeSearch.finish(msg0)


plugin_name_2 = "anime-setu"
key_LoliconAPI = config['api']['LoliconAPI']
setu_type = 2  # setu-type: 1(local), 2(url: https://api.lolicon.app/#/setu)
SP_temp_list = []
SP_list = []


def check_sepi() -> Rule:
    """检查目标是否是涩批"""
    async def _check_sepi(bot: Bot, event: Event, state: dict) -> bool:
        if event.user_id in SP_list:
            await bot.send(event, "你可少冲点吧！涩批！哼唧")
            return False
        else:
            return True
    return Rule(_check_sepi)

def add_sepi(user: int) -> None:
    """将目标移入涩批名单"""
    global SP_list
    SP_list.append(user)

def del_sepi(user: int) -> None:
    """将目标移出涩批名单"""
    global SP_list
    SP_list.remove(user)


setu = on_regex(
    r"来[点丶张份副个幅][涩色瑟][图圖]|[涩色瑟][图圖]来|[涩色瑟][图圖][gkd|GKD|搞快点]|[gkd|GKD|搞快点][涩色瑟][图圖]",
    rule=check_banlist() & check_switch(plugin_name_2, False) & check_sepi())


@setu.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
    global SP_temp_list
    user = event.user_id
    group = event.group_id
    res = randint(1, 5)
    print(1)

    if countX(SP_temp_list, user) == 5:
        add_sepi(user) # type: ignore
        SP_temp_list = list(set(SP_temp_list))
        delta = timedelta(hours=1)
        trigger = DateTrigger(run_date=datetime.now() + delta)
        scheduler.add_job(func=del_sepi,
                          trigger=trigger,
                          args=(user, ),
                          misfire_grace_time=60)
        return

    if setu_type == 1:

        DATA_PATH = Path('.') / 'ATRI' / 'data' / 'data_Sqlite' / 'setu' / 'nearR18.db'
        
        if not DATA_PATH.is_file():
            await setu.finish("数据库...她是空的！！！")
        
        con = sqlite3.connect(DATA_PATH)
        cur = con.cursor()
        msg = cur.execute('SELECT * FROM nearR18 ORDER BY RANDOM() limit 1;')

        for i in msg:
            pid = i[0]
            title = i[1]
            img = i[7]

            msg0 = "setu info:\n"
            msg0 += f"Title: {title}\n"
            msg0 += f"Pid: {pid}\n"
            msg0 += f"[CQ:image,file=file:///{compress_image(await aio_download_pics(img))}]"

            if 1 <= res < 5:
                SP_temp_list.append(user)
                await setu.finish(msg0)

            elif res == 5:
                await bot.send(event, "我找到涩图了！但我发给主人了\nο(=•ω＜=)ρ⌒☆")

                for sup in config['bot']['superusers']:
                    await bot.send_private_msg(
                        user_id=sup,
                        message=
                        f"主人，从群{group}来的涩图！热乎着！\nTitle: {title}\nPid: {pid}\n[CQ:image,file=file:///{compress_image(await aio_download_pics(img))}]"
                    )

    else:
        params = {"apikey": key_LoliconAPI, "r18": "0", "num": "1"}

        data = {}

        try:
            data = json.loads(
                request_get('https://api.lolicon.app/setu/', params))
        except Exception:
            await setu.finish(errorRepo("请求数据失败，也可能为接口调用次数达上限"))

        msg0 = "setu info:\n"
        msg0 += f'Title: {data["data"][0]["title"]}\n'
        msg0 += f'Pid: {data["data"][0]["pid"]}\n'
        msg0 += f'[CQ:image,file=file:///{compress_image(await aio_download_pics(data["data"][0]["url"]))}]'

        if 1 <= res < 5:
            SP_temp_list.append(user)
            await setu.finish(msg0)

        elif res == 5:
            await bot.send(event, "我找到涩图了！但我发给主人了\nο(=•ω＜=)ρ⌒☆")

            for sup in config['bot']['superusers']:
                await bot.send_private_msg(
                    user_id=sup,
                    message=
                    f'主人，从群{group}来的涩图！热乎着！\nTitle: {data["data"][0]["title"]}\nPid: {data["data"][0]["pid"]}\n[CQ:image,file=file:///{compress_image(await aio_download_pics(data["data"][0]["url"]))}]'
                )


setuType = on_command("setu-type", permission=SUPERUSER)


@setuType.handle()
async def _(bot: Bot, event: Event, state: dict) -> None:
    global setu_type
    msg = str(event.message).strip()

    if not msg:
        await setuType.finish("请查看文档获取帮助（")

    if msg == "local":
        setu_type = 1

    elif msg == "url":
        setu_type = 2

    else:
        await setuType.finish("请检查类型是否输入正确嗷！")

    await setuType.finish("Type conversion completed!")
