import os
import time
import json
import asyncio
import sqlite3
import nonebot

from pathlib import Path
from nonebot import on_command, CommandSession

import config
from ATRI.modules.response import request_api


bot = nonebot.get_bot()
master = config.SUPERUSERS
url = f'https://api.imjad.cn/pixiv/v1/?type=illust&id='


try:
    with open(Path('.') / 'ATRI' / 'plugins' / 'UploadSqlite' / 'sepi.json', 'r') as f:
        sP = json.load(f)
except:
    sP = {}
sepi = list(sP.keys())

try:
    with open(Path('.') / 'ATRI' / 'plugins' / 'UploadSqlite' / 'cloudmusic.json', 'r') as f:
        cD = json.load(f)
except:
    cD = {}
cloudmusic = list(cD.keys())



@on_command('upload_setu', aliases = ['上传涩图'], only_to_me = False)
async def _(session: CommandSession):
    user = session.event.user_id
    if user in master or user in sepi:
        start = time.perf_counter()
        msg = session.event.raw_message.split(' ', 2)
        print(msg)
        i_tpye = msg[1]
        pid = msg[2] 

        URL = url + pid

        dc = json.loads(request_api(URL))
        if not dc:
            session.finish('ATRI在尝试解析数据时出问题...等会再试试吧...')
        title = dc["response"][0]["title"]
        tags = dc["response"][0]["tags"]
        account = dc["response"][0]["user"]["account"]
        name = dc["response"][0]["user"]["name"]
        u_id = dc["response"][0]["user"]["id"]
        user_link = f'https://www.pixiv.net/users/' + f'{u_id}'
        img = f'https://pixiv.cat/{pid}.jpg'

        dataSETU = (f'{pid}', f'{title}', f'{tags}', f'{account}', f'{name}', f'{u_id}', f'{user_link}', f'{img}')

        if i_tpye == '正常':
            if os.path.exists('ATRI/data/sqlite/setu/normal.db'):
                print('数据文件存在！')
            else:
                await session.send('数据库不存在，将在3秒后开始构建...')
                await asyncio.sleep(3)
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
            cur.execute('INSERT INTO normal(pid, title, tags, account, name, u_id, user_link, img) VALUES(?, ?, ?, ?, ?, ?, ?, ?)', dataSETU)
            con.commit()
            con.close()

        elif i_tpye == '擦边球':
            if os.path.exists('ATRI/data/sqlite/setu/nearR18.db'):
                print('数据文件存在！')
            else:
                await session.send('数据库不存在，将在3秒后开始构建...')
                await asyncio.sleep(3)
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
            cur.execute('INSERT INTO nearR18(pid, title, tags, account, name, u_id, user_link, img) VALUES(?, ?, ?, ?, ?, ?, ?, ?)', dataSETU)
            con.commit()
            con.close()

        elif i_tpye == 'r18':
            if os.path.exists('ATRI/data/sqlite/cloudmusic/cloudmusic.db'):
                print('数据文件存在！')
            else:
                await session.send('数据库不存在，将在3秒后开始构建...')
                await asyncio.sleep(3)
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
            cur.execute('INSERT INTO r18(pid, title, tags, account, name, u_id, user_link, img) VALUES(?, ?, ?, ?, ?, ?, ?, ?)', dataSETU)
            con.commit()
            con.close()
        
        end = time.perf_counter()
        
        await session.send(f'数据上传完成！\n耗时: {round(end - start, 3)}s')

@on_command('upload_cloudmusic', aliases = ['上传网抑语', '网抑云', '网易云'], only_to_me = False)
async def _(session: CommandSession):
    user = session.event.user_id
    if user in master or user in cloudmusic:
        start = time.perf_counter()
        msg = session.event.raw_message.split(' ', 1)
        msg = msg[1]

        if os.path.exists('ATRI/data/sqlite/cloudmusic/cloudmusic.db'):
                print('数据文件存在！')
        else:
            await session.send('数据库不存在，将在3秒后开始构建...')
            await asyncio.sleep(3)
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
        cur.execute('INSERT INTO cloudmusic(msg) VALUES (?)', msg)
        con.commit()
        con.close()

        end = time.perf_counter()

        await session.send(f'数据上传完成！\n耗时: {round(end - start, 3)}s')


@on_command('del_setu', aliases = ['删除涩图'], only_to_me = False)
async def _(session: CommandSession):
    user = session.event.user_id
    if user in master or user in sepi:
        start = time.perf_counter()
        msg = session.event.raw_message.split(' ', 2)
        i_tpye = msg[1]
        pid = msg[2]

        if i_tpye == '正常':
            if os.path.exists(Path('.') / 'ATRI' / 'data' / 'sqlite' / 'setu' / 'normal.db'):
                print('数据文件存在！')
            else:
                session.finish('ERROR: 恁都没库删锤子')
            con = sqlite3.connect(Path('.') / 'ATRI' / 'data' / 'sqlite' / 'setu' / 'normal.db')
            cur = con.cursor()
            cur.execute(f'DELETE FROM COMPANY WHERE ID = {pid}')
            con.commit()
            con.close()
        
        elif i_tpye == '擦边球':
            if os.path.exists(Path('.') / 'ATRI' / 'data' / 'sqlite' / 'setu' / 'nearR18.db'):
                print('数据文件存在！')
            else:
                session.finish('ERROR: 恁都没库删锤子')
            con = sqlite3.connect(Path('.') / 'ATRI' / 'data' / 'sqlite' / 'setu' / 'nearR18.db')
            cur = con.cursor()
            cur.execute(f'DELETE FROM COMPANY WHERE ID = {pid}')
            con.commit()
            con.close()
        

        elif i_tpye == 'r18':
            if os.path.exists(Path('.') / 'ATRI' / 'data' / 'sqlite' / 'setu' / 'r18.db'):
                print('数据文件存在！')
            else:
                session.finish('ERROR: 恁都没库删锤子')
            con = sqlite3.connect(Path('.') / 'ATRI' / 'data' / 'sqlite' / 'setu' / 'r18.db')
            cur = con.cursor()
            cur.execute(f'DELETE FROM COMPANY WHERE ID = {pid}')
            con.commit()
            con.close()
        
        end = time.perf_counter()
        
        await session.send(f'数据删除完成！\n耗时: {round(end - start, 3)}s')

@on_command('del_cloudmusic', aliases = ['删除网易云'], only_to_me = False)
async def _(session: CommandSession):
    user = session.event.user_id
    if user in master or user in cloudmusic:
        start = time.perf_counter()
        msg = session.event.raw_message.split(' ', 1)
        msg = msg[1]

        if os.path.exists('ATRI/data/sqlite/cloudmusic/cloudmusic.db'):
            print('数据文件存在！')
        else:
            session.finish('ERROR: 恁都没库删锤子')
        con = sqlite3.connect(Path('.') / 'ATRI' / 'data' / 'sqlite' / 'cloudmusic' / 'cloudmusic.db')
        cur = con.cursor()
        cur.execute('INSERT INTO cloudmusic(msg) VALUES (?)', msg)
        con.commit()
        con.close()

        end = time.perf_counter()

        await session.send(f'数据删除完成！\n耗时: {round(end - start, 3)}s')


@on_command('add_check_sepi', aliases=['添加涩批', '移除涩批'], only_to_me = False)
async def _(session: CommandSession):
    if session.event.user_id in master:
        msg = session.event.raw_message.split(' ', 1)
        m_type = msg[0]
        u = msg[1]

        if m_type == '添加涩批':
            try:
                with open(Path('.') / 'ATRI' / 'plugins' / 'UploadSqlite' / 'sepi.json', 'r') as f:
                    data = json.load(f)
            except:
                data = {}
            
            data[f"{u}"] = f"{u}"
            f = open(Path('.') / 'ATRI' / 'plugins' / 'UploadSqlite' / 'sepi.json', 'w')
            f.write(json.dumps(data))
            f.close()
            await session.send(f'成功添加涩批[{u}]！')
        
        elif m_type == '移除涩批':
            try:
                with open(Path('.') / 'ATRI' / 'plugins' / 'UploadSqlite' / 'sepi.json', 'r') as f:
                    data = json.load(f)
            except:
                data = {}
            
            data.pop(f"{u}")
            f = open(Path('.') / 'ATRI' / 'plugins' / 'UploadSqlite' / 'sepi.json', 'w')
            f.write(json.dumps(data))
            f.close()
            await session.send(f'成功移除涩批[{u}]！')

@on_command('add_check_cd', aliases = ['添加抑郁', '移除抑郁'], only_to_me = False)
async def _(session: CommandSession):
    if session.event.user_id in master:
        msg = session.event.raw_message.split(' ', 1)
        m_type = msg[0]
        u = msg[1]

        if m_type == '添加抑郁':
            try:
                with open(Path('.') / 'ATRI' / 'plugins' / 'UploadSqlite' / 'cloudmusic.json', 'r') as f:
                    data = json.load(f)
            except:
                data = {}
            
            data[f"{u}"] = f"{u}"
            f = open(Path('.') / 'ATRI' / 'plugins' / 'UploadSqlite' / 'cloudmusic.json', 'w')
            f.write(json.dumps(data))
            f.close()
            await session.send(f'成功添加抑郁[{u}]！')
        
        elif m_type == '移除抑郁':
            try:
                with open(Path('.') / 'ATRI' / 'plugins' / 'UploadSqlite' / 'cloudmusic.json', 'r') as f:
                    data = json.load(f)
            except:
                data = {}
            
            data.pop(f"{u}")
            f = open(Path('.') / 'ATRI' / 'plugins' / 'UploadSqlite' / 'cloudmusic.json', 'w')
            f.write(json.dumps(data))
            f.close()
            await session.send(f'成功移除抑郁[{u}]！')