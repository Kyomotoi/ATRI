#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2020/10/11 14:38:14
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

from nonebot.log import logger
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.plugin import on_message, on_command, on_regex

from utils.utils_banList import banList
from utils.utils_error import errorRepo
from utils.utils_history import getMessage
from utils.utils_switch import checkSwitch
from utils.utils_translate import toSimpleString
from utils.utils_request import aio_get_bytes, request_get
from utils.utils_img import compress_image, aio_download_pics

from .body import resultRepo
import ATRI


plugin_name_0 = "anime-pic-search"
key_SauceNAO = ATRI.key_SauceNaoKEY

SaucenaoSearch = on_command('以图搜图')

@SaucenaoSearch.handle() # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
    user = str(event.user_id)
    group = str(event.group_id)

    state["user"] = user
    state["group"] = group

    if banList(user, group):
        if checkSwitch(plugin_name_0, group):
            img = str(event.message).strip()
            
            if img:
                state["img_url"] = img
        else:
            await SaucenaoSearch.finish(f"Service-{plugin_name_0} has been closed.")

@SaucenaoSearch.got("img_url", prompt="请发送一张目标图片") # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
    img = state["img_url"]
    img = re.findall(r"(http://.*?)]", img)

    if len(img):
        pass
    else:
        await SaucenaoSearch.reject("请发送一张目标图片，而非文字或其他非图片成分( -'`-; )")
    
    await bot.send(event, "别急！正在找图！")

    await SaucenaoSearch.finish(resultRepo(state['user'], key_SauceNAO, img[0]))


SaucenaoSearch_repo = on_message()

@SaucenaoSearch_repo.handle() # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
    user = str(event.user_id)
    group = str(event.group_id)
    msg = str(event.message)

    if banList(user, group):
        if checkSwitch(plugin_name_0, group):
            if "[CQ:reply" in msg:
                if "搜图" in msg or "识图" in msg:
                    if group == "None":
                        await SaucenaoSearch_repo.finish("ごめんなさい...\n该功能只对群聊开放哦~~")
                    
                    try:
                        repo_info = re.findall(r"CQ:reply,id=([0-9]\S+)]", msg)
                        msg_id = repo_info[0]
                    except Exception:
                        logger.warning(f"Get message_id ERROR!")
                        await SaucenaoSearch_repo.finish(errorRepo('定位消息内容失败'))
                        return
                    
                    aim = getMessage(msg_id)[f"{msg_id}"]["message"]
                    img = img = re.findall(r"(http://.*?)]", aim)

                    if len(img):
                        pass
                    else:
                        await SaucenaoSearch_repo.finish('这消息内貌似没图片呢...')
                    
                    await bot.send(event, "别急！正在找图！")

                    await SaucenaoSearch.finish(resultRepo(state['user'], key_SauceNAO, img[0]))

        else:
            await SaucenaoSearch.finish(f"Service-{plugin_name_0} has been closed.")


plugin_name_1 = "anime-vid-search"

AnimeSearch = on_command('以图搜番')

@AnimeSearch.handle() # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
    user = str(event.user_id)
    group = str(event.group_id)

    state["user"] = user
    state["group"] = group

    if banList(user, group):
        if checkSwitch(plugin_name_1, group):
            img = str(event.message).strip()

            if img:
                state["img_url"] = img
        else:
            await AnimeSearch.finish(f"Service-{plugin_name_1} has been closed.")

@AnimeSearch.got("img_url", prompt="请发送一张目标图片") # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
    img = state["img_url"]
    img = re.findall(r"(http://.*?)]", img)

    if len(img):
        pass
    else:
        await SaucenaoSearch.reject("请发送一张目标图片，而非文字或其他非图片成分( -'`-; )")
    
    await bot.send(event, "别急！正在搜索！")
    
    URL = f'https://trace.moe/api/search?url={img[0]}'
    try:
        req = await aio_get_bytes(URL)
    except:
        await AnimeSearch.finish(errorRepo("请求数据失败"))
    
    data = json.loads(req.decode()) # type: ignore

    try:
        d = {}

        for i in range(len(data['docs'])):
            if data['docs'][i]['title_chinese'] in d:
                d[data['docs'][i]['title_chinese']][0] += data['docs'][i]['similarity']
            
            else:
                m = data['docs'][i]['at']/60
                s = data['docs'][i]['at']%60

                if data['docs'][i]['episode'] == '':
                    n = 1
                
                else:
                    n = data['docs'][i]['episode']
                
                d[toSimpleString(data['docs'][i]['title_chinese'])] = [data['docs'][i]['similarity'],f'第{n}集',f'{int(m)}分{int(s)}秒处']
    except:
        await AnimeSearch.finish(errorRepo("处理数据失败"))
    
    result = sorted(
        d.items(), # type: ignore
        key=lambda x:x[1],
        reverse=True)
    
    t = 0
    msg0 = f'[CQ:at,qq={state["user"]}]\n根据所提供的图片按照相似度找到{len(d)}个结果:' # type: ignore

    for i in result:
        t +=1
        lk = ('%.2f%%' % (i[1][0] * 100))
        msg = (f'\n——————————\n({t})\n相似度：{lk}\n动漫名：《{i[0]}》\n时间点：{i[1][1]} {i[1][2]}')
        msg0 += msg
    
    await AnimeSearch.finish(msg0)


plugin_name_2 = "anime-setu"
key_LoliconAPI = ATRI.key_LoliconAPI
setu_type = 1  # setu-type: 1(local), 2(url: https://api.lolicon.app/#/setu) default: 1(local)

setu = on_regex(r"来[点丶张份副个幅][涩色瑟][图圖]|[涩色瑟][图圖]来|[涩色瑟][图圖][gkd|GKD|搞快点]|[gkd|GKD|搞快点][涩色瑟][图圖]")

@setu.handle() # type: ignore
async def _setu(bot: Bot, event: Event, state: dict) -> None:
    user = str(event.user_id)
    group = str(event.group_id)

    if banList(user, group):
        if checkSwitch(plugin_name_2, group):

            res = randint(1,5)

            if setu_type == 1:

                con = sqlite3.connect(Path('.') / 'ATRI' / 'data' / 'data_Sqlite' / 'setu' / 'nearR18.db')
                cur = con.cursor()
                msg = cur.execute('SELECT * FROM nearR18 ORDER BY RANDOM() limit 1;')

                for i in msg:
                    pid = i[0]
                    title = i[1]
                    img = i[7]
                    
                    msg0 = f"setu info:\n"
                    msg0 += f"Title: {title}\n"
                    msg0 += f"Pid: {pid}\n"
                    msg0 += f"[CQ:image,file=file:///{compress_image(await aio_download_pics(img))}]"
                    
                    if 1 <= res < 5:
                        await setu.finish(msg0)

                    elif res == 5:
                        await bot.send(event, "我找到涩图了！但我发给主人了\nο(=•ω＜=)ρ⌒☆")

                        await bot.send_private_msg(
                            user_id=ATRI.config_SUPERUSERS,
                            message=f"主人，从群{group}来的涩图！热乎着！\nTitle: {title}\nPid: {pid}\n[CQ:image,file=file:///{compress_image(await aio_download_pics(img))}]"
                        )
            
            else:
                params = {
                    "apikey": key_LoliconAPI,
                    "r18": "0",
                    "num": "1"
                }

                data = {}

                try:
                    data = json.loads(request_get('https://api.lolicon.app/setu/', params))
                except Exception:
                    await setu.finish(errorRepo("请求数据失败，也可能为接口调用次数达上限"))
                
                msg0 = f"setu info:\n"
                msg0 += f'Title: {data["data"][0]["title"]}\n'
                msg0 += f'Pid: {data["data"][0]["pid"]}\n'
                msg0 += f'[CQ:image,file=file:///{compress_image(await aio_download_pics(data["data"][0]["url"]))}]'

                if 1 <= res < 5:
                    await setu.finish(msg0)
                
                elif res == 5:
                    await bot.send(event, "我找到涩图了！但我发给主人了\nο(=•ω＜=)ρ⌒☆")

                    await bot.send_private_msg(
                        user_id=ATRI.config_SUPERUSERS,
                        message=f'主人，从群{group}来的涩图！热乎着！\nTitle: {data["data"][0]["title"]}\nPid: {data["data"][0]["pid"]}\n[CQ:image,file=file:///{compress_image(await aio_download_pics(data["data"][0]["url"]))}]'
                    )
            
        else:
            await setu.finish(f"Service-{plugin_name_2} has been closed.")

setuType = on_command("setu-type", permission=SUPERUSER)

@setuType.handle() # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
    global setu_type
    msg = str(event.message).strip()

    if msg:
        pass
    else:
        msg0 = "-==ATRI Setu Type Control System==-\n"
        msg0 += "**Tips: For SUPERUSERS**\n"
        msg0 += "┌Usage: setu-type {type}\n"
        msg0 += "└Type:\n"
        msg0 += "  ├local\n"
        msg0 += "  └url"

        await setuType.finish(msg0)
    
    if msg == "local":
        setu_type = 1
    
    elif msg == "url":
        setu_type = 2
    
    else:
        await setuType.finish("请检查类型是否输入正确嗷！")
    
    await setuType.finish("Type conversion completed!")


# @scheduler.scheduled_job(
#     "cron",
#     minute=45,
#     bot=Bot,
#     event=Event,
#     state=dict
#     )
# async def _(bot: Bot, event: Event, state: dict) -> None:
#     group = str(event.group_id)

#     if banList(group=group):
#         if checkSwitch(plugin_name_2, group):
#             # group_list = await bot.get_group_list()
#             # group = sample(group_list, 1)
#             # group = group['group_id']

#             if setu_type == 1:

#                 con = sqlite3.connect(Path('.') / 'ATRI' / 'data' / 'data_Sqlite' / 'setu' / 'nearR18.db')
#                 cur = con.cursor()
#                 msg = cur.execute('SELECT * FROM nearR18 ORDER BY RANDOM() limit 1;')

#                 for i in msg:
#                     pid = i[0]
#                     title = i[1]
#                     img = i[7]
                    
#                     msg0 = f"setu info:\n"
#                     msg0 += f"Title: {title}\n"
#                     msg0 += f"Pid: {pid}\n"
#                     msg0 += f"[CQ:image,file=file:///{compress_image(await aio_download_pics(img))}]"
                    
#                     await setu.finish(msg0)
            
#             else:
#                 params = {
#                     "apikey": key_LoliconAPI,
#                     "r18": "0",
#                     "num": "1"
#                 }

#                 data = {}

#                 try:
#                     data = json.loads(request_get('https://api.lolicon.app/setu/', params))
#                 except Exception:
#                     await setu.finish(errorRepo("请求数据失败，也可能为接口调用次数达上限"))
                
#                 msg0 = f"setu info:\n"
#                 msg0 += f'Title: {data["data"][0]["title"]}\n'
#                 msg0 += f'Pid: {data["data"][0]["pid"]}\n'
#                 msg0 += f'[CQ:image,file=file:///{compress_image(await aio_download_pics(data["data"][0]["url"]))}]'

#                 await setu.finish(msg0)
