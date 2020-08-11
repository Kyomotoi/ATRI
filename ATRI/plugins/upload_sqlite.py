# -*- coding:utf-8 -*-
import os
import time
import json
import sqlite3
import nonebot

from pathlib import Path
from nonebot import on_command, CommandSession

from ATRI.modules import response # type: ignore


bot = nonebot.get_bot()
master = bot.config.SUPERUSERS # type: ignore
url = f'https://api.imjad.cn/pixiv/v1/?type=illust&id='


@on_command('upload_setu', aliases = ['上传涩图'], only_to_me = False)
async def _(session: CommandSession):
    if session.event.user_id in master:
        start = time.perf_counter()
        msg = session.event.raw_message.split(' ', 2)
        print(msg)
        i_tpye = msg[1]
        pid = msg[2] 

        URL = url + pid

        dc = json.loads(response.request_api(URL))
        if not dc:
            session.finish('ATRI在尝试解析数据时出问题...等会再试试吧...')
        title = dc["response"][0]["title"]
        tags = dc["response"][0]["tags"]
        account = dc["response"][0]["user"]["account"]
        name = dc["response"][0]["user"]["name"]
        u_id = dc["response"][0]["user"]["id"]
        user_link = f'https://www.pixiv.net/users/' + f'{u_id}'
        img = f'https://pixiv.cat/{pid}.jpg'

        if i_tpye == '正常':
            if os.path.exists('ATRI/data/sqlite/setu/normal.db'):
                print('数据文件存在！')
            else:
                await session.send('数据库不存在，将在3秒后开始构建...')
                time.sleep(3)
                await session.send('开始构建数据库！')
                con = sqlite3.connect(Path('.') / 'ATRI' / 'data' / 'sqlite' / 'setu' / 'normal.db')
                cur = con.cursor()
                cur.execute('CREATE TABLE normal(pid PID, title TITLE, tags TAGS, account ACCOUNT, name NAME, u_id UID, user_link USERLINK, img IMG, UNIQUE(pid, title, tags, account, name, u_id, user_link, img))')
                con.commit()
                cur.close()
                con.close()
                await session.send('完成')
     
            con = sqlite3.connect(Path('.') / 'ATRI' / 'data' / 'sqlite' / 'setu' / 'normal.db')
            cur = con.cursor()
            cur.execute('INSERT INTO normal VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")'%(pid, title, tags, account, name, u_id, user_link, img))
            con.commit()
            con.close()

        elif i_tpye == '擦边球':
            if os.path.exists('ATRI/data/sqlite/setu/nearR18.db'):
                print('数据文件存在！')
            else:
                await session.send('数据库不存在，将在3秒后开始构建...')
                time.sleep(3)
                await session.send('开始构建数据库！')
                con = sqlite3.connect(Path('.') / 'ATRI' / 'data' / 'sqlite' / 'setu' / 'nearR18.db')
                cur = con.cursor()
                cur.execute('CREATE TABLE nearR18(pid PID, title TITLE, tags TAGS, account ACCOUNT, name NAME, u_id UID, user_link USERLINK, img IMG, UNIQUE(pid, title, tags, account, name, u_id, user_link, img))')
                con.commit()
                cur.close()
                con.close()
                await session.send('完成')
 
            con = sqlite3.connect(Path('.') / 'ATRI' / 'data' / 'sqlite' / 'setu' / 'nearR18.db')
            cur = con.cursor()
            cur.execute('INSERT INTO nearR18 VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")'%(pid, title, tags, account, name, u_id, user_link, img))
            con.commit()
            con.close()

        elif i_tpye == 'r18':
            if os.path.exists('ATRI/data/sqlite/cloudmusic/cloudmusic.db'):
                print('数据文件存在！')
            else:
                await session.send('数据库不存在，将在3秒后开始构建...')
                time.sleep(3)
                await session.send('开始构建数据库！')
                con = sqlite3.connect(Path('.') / 'ATRI' / 'data' / 'sqlite' / 'setu' / 'r18.db')
                cur = con.cursor()
                cur.execute('CREATE TABLE r18(pid PID, title TITLE, tags TAGS, account ACCOUNT, name NAME, u_id UID, user_link USERLINK, img IMG, UNIQUE(pid, title, tags, account, name, u_id, user_link, img))')
                con.commit()
                cur.close()
                con.close()
                await session.send('完成')

            con = sqlite3.connect(Path('.') / 'ATRI' / 'data' / 'sqlite' / 'setu' / 'r18.db')
            cur = con.cursor()
            cur.execute('INSERT INTO r18 VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")'%(pid, title, tags, account, name, u_id, user_link, img))
            con.commit()
            con.close()
        
        end = time.perf_counter()
        
        await session.send(f'数据上传完成！\n耗时: {round(end - start, 3)}s')

@on_command('upload_cloudmusic', aliases = ['上传网抑语', '网抑云', '网易云'], only_to_me = False)
async def _(session: CommandSession):
    if session.event.user_id in master:
        start = time.perf_counter()
        msg = session.event.raw_message.split(' ', 1)
        msg = msg[1]

        if os.path.exists('ATRI/data/sqlite/cloudmusic/cloudmusic.db'):
                print('数据文件存在！')
        else:
            await session.send('数据库不存在，将在3秒后开始构建...')
            time.sleep(3)
            await session.send('开始构建数据库！')
            con = sqlite3.connect(Path('.') / 'ATRI' / 'data' / 'sqlite' / 'cloudmusic' / 'cloudmusic.db')
            cur = con.cursor()
            cur.execute('CREATE TABLE cloudmusic(msg MSG, UNIQUE(msg))')
            con.commit()
            cur.close()
            con.close()
            await session.send('完成')
 
        con = sqlite3.connect(Path('.') / 'ATRI' / 'data' / 'sqlite' / 'cloudmusic' / 'cloudmusic.db')
        cur = con.cursor()
        cur.execute('INSERT INTO cloudmusic VALUES ("%s")'%(msg))
        con.commit()
        con.close()

        end = time.perf_counter()

        await session.send(f'数据上传完成！\n耗时: {round(end - start, 3)}s')


@on_command('data_list', aliases = ['查看上传数据', '数据总量'], only_to_me = False)
async def _(session: CommandSession):
    user = session.event.user_id
    with open('ATRI/plugins/noobList/noobList.json', 'r') as f:
        data = json.load(f)

    if data[f"{user}"] == str(user):
        pass
    else:
        con = sqlite3.connect(Path('.') / 'ATRI' / 'data' / 'sqlite' / 'setu' / 'normal.db') # setu-normal
        cur = con.cursor()
        cur.execute("select * from normal")
        data_normal = len(cur.fetchall())
        con.close()

        con = sqlite3.connect(Path('.') / 'ATRI' / 'data' / 'sqlite' / 'setu' / 'nearR18.db') # setu-nearR18
        cur = con.cursor()
        cur.execute("select * from nearR18")
        data_nearR18 = len(cur.fetchall())
        con.close()

        con = sqlite3.connect(Path('.') / 'ATRI' / 'data' / 'sqlite' / 'setu' / 'r18.db') # setu-r18
        cur = con.cursor()
        cur.execute("select * from r18")
        data_r18 = len(cur.fetchall())
        con.close()

        con = sqlite3.connect(Path('.') / 'ATRI' / 'data' / 'sqlite' / 'cloudmusic' / 'cloudmusic.db') # cloudmusic
        cur = con.cursor()
        cur.execute("select * from cloudmusic")
        data_cloudmusic = len(cur.fetchall())
        con.close()

        await session.send(
            f"""目前螃蟹™数据库收录了：
    涩图：
        normal: {data_normal}
        nearR18: {data_nearR18}
        r18：{data_r18}
    网抑云语录：{data_cloudmusic}"""
        )