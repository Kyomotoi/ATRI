#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2020/10/25 15:01:29
@Author  :   Kyomotoi
@Contact :   kyomotoiowo@gmail.com
@Github  :   https://github.com/Kyomotoi
@License :   Copyright © 2018-2020 Kyomotoi, All Rights Reserved.
'''
__author__ = 'kyomotoi'

import os
import json
import sqlite3
from pathlib import Path
from nonebot.plugin import on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import Bot, Event

from utils.utils_error import errorRepo
from utils.utils_request import aio_get_bytes


UploadSetu = on_command('setu', permission=SUPERUSER)

@UploadSetu.handle() # type: ignore
async def _(bot: Bot, event: Event, state: dict) -> None:
    msg = str(event.message).strip().split(' ')

    s_type = msg[0]
    pid = msg[1]

    URL = f'https://api.imjad.cn/pixiv/v1/?type=illust&id={pid}'
    info = {}

    try:
        info = json.loads(await aio_get_bytes(URL))
    except:
        await UploadSetu.finish(errorRepo("网络请求出错"))
    
    info = info["response"][0]
    title = info["title"]
    tags = info["tags"]
    account = info["account"]
    name = info["user"]["name"]
    u_id = info["user"]["id"]
    user_link = f'https://www.pixiv.net/users/' + f'{u_id}'
    img = f'https://pixiv.cat/{pid}.jpg'

    data_setu = (f'{pid}', f'{title}', f'{tags}', f'{account}', f'{name}', f'{u_id}', f'{user_link}', f'{img}')

    if s_type == "normal":
        if os.path.exists('ATRI/data/data_Sqlite/setu/normal.db'):
            print('数据文件存在！')
        else:
            await bot.send(event, '数据库不存在，将开始构建...')
            await bot.send(event, '开始构建数据库！')
            con = sqlite3.connect(Path('.') / 'ATRI' / 'data' / 'data_Sqlite' / 'setu' / 'normal.db')
            cur = con.cursor()
            cur.execute('CREATE TABLE normal(pid PID, title TITLE, tags TAGS, account ACCOUNT, name NAME, u_id UID, user_link USERLINK, img IMG, UNIQUE(pid, title, tags, account, name, u_id, user_link, img))')
            con.commit()
            cur.close()
            await bot.send(event, '完成')
        
        con = sqlite3.connect(Path('.') / 'ATRI' / 'data' / 'data_Sqlite' / 'setu' / 'normal.db')
        cur = con.cursor()
        cur.execute('INSERT INTO normal(pid, title, tags, account, name, u_id, user_link, img) VALUES(?, ?, ?, ?, ?, ?, ?, ?)', data_setu)
        con.commit()
        con.close()
    
    elif s_type == "nearr18":
        if os.path.exists('ATRI/data/data_Sqlite/setu/nearR18.db'):
            print('数据文件存在！')
        else:
            await bot.send(event, '数据库不存在，将开始构建...')
            await bot.send(event, '开始构建数据库！')
            con = sqlite3.connect(Path('.') / 'ATRI' / 'data' / 'data_Sqlite' / 'setu' / 'nearR18.db')
            cur = con.cursor()
            cur.execute('CREATE TABLE nearR18(pid PID, title TITLE, tags TAGS, account ACCOUNT, name NAME, u_id UID, user_link USERLINK, img IMG, UNIQUE(pid, title, tags, account, name, u_id, user_link, img))')
            con.commit()
            cur.close()
            await bot.send(event, '完成')
    
        con = sqlite3.connect(Path('.') / 'ATRI' / 'data' / 'data_Sqlite' / 'setu' / 'nearR18.db')
        cur = con.cursor()
        cur.execute('INSERT INTO nearR18(pid, title, tags, account, name, u_id, user_link, img) VALUES(?, ?, ?, ?, ?, ?, ?, ?)', data_setu)
        con.commit()
        con.close()
    
    elif s_type == "r18":
        if os.path.exists('ATRI/data/data_Sqlite/setu/r18.db'):
            print('数据文件存在！')
        else:
            await bot.send(event, '数据库不存在，将开始构建...')
            await bot.send(event, '开始构建数据库！')
            con = sqlite3.connect(Path('.') / 'ATRI' / 'data' / 'data_Sqlite' / 'setu' / 'r18.db')
            cur = con.cursor()
            cur.execute('CREATE TABLE r18(pid PID, title TITLE, tags TAGS, account ACCOUNT, name NAME, u_id UID, user_link USERLINK, img IMG, UNIQUE(pid, title, tags, account, name, u_id, user_link, img))')
            con.commit()
            cur.close()
            await bot.send(event, '完成')
    
        con = sqlite3.connect(Path('.') / 'ATRI' / 'data' / 'data_Sqlite' / 'setu' / 'r18.db')
        cur = con.cursor()
        cur.execute('INSERT INTO r18(pid, title, tags, account, name, u_id, user_link, img) VALUES(?, ?, ?, ?, ?, ?, ?, ?)', data_setu)
        con.commit()
        con.close()

    await UploadSetu.finish(f"数据上传完成~！\n涩图库[{s_type}]涩图 +1")
