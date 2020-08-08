import os
import re
import time
import json
import sqlite3
from random import choice
from pathlib import Path
from iotbot import GroupMsg
from iotbot import decorators as deco
from iotbot.action import Action
from iotbot.sugar import Text

from tools import response #type: ignore
import config_ #type: ignore


bot = config_.BOT_QQ()
master = config_.MASTER() # type: ignore
url = f'https://api.imjad.cn/pixiv/v1/?type=illust&id='


@deco.not_botself
def receive_group_msg(ctx: GroupMsg):
    msg = ctx.Content
    if re.findall(r"(上传涩图)", msg):
        if ctx.FromUserId == master:
            start = time.perf_counter()
            msg = msg.split(' ', 2)
            print(msg)
            i_tpye = msg[1]
            pid = msg[2]

            URL = url + pid

            dc = json.loads(response.request_api(URL))
            if not dc:
                Text('ATRI在尝试解析数据时出问题...等会再试试吧...')
                return
            title = dc["response"][0]["title"]
            tags = dc["response"][0]["tags"]
            account = dc["response"][0]["user"]["account"]
            name = dc["response"][0]["user"]["name"]
            u_id = dc["response"][0]["user"]["id"]
            user_link = f'https://www.pixiv.net/users/' + f'{u_id}'
            img = f'https://pixiv.cat/{pid}.jpg'

            if i_tpye == '正常':
                if os.path.exists('data/sqlite/setu/normal.db'):
                    print('数据文件存在！')
                else:
                    Text('数据库不存在，将在3秒后开始构建...')
                    time.sleep(3)
                    Text('开始构建数据库！')
                    con = sqlite3.connect(Path('.') / 'data' / 'sqlite' / 'setu' / 'normal.db')
                    cur = con.cursor()
                    cur.execute('CREATE TABLE normal(pid PID, title TITLE, tags TAGS, account ACCOUNT, name NAME, u_id UID, user_link USERLINK, img IMG, UNIQUE(pid, title, tags, account, name, u_id, user_link, img))')
                    con.commit()
                    cur.close()
                    con.close()
                    Text('完成')
        
                con = sqlite3.connect(Path('.') / 'data' / 'sqlite' / 'setu' / 'normal.db')
                cur = con.cursor()
                cur.execute('INSERT INTO normal VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")'%(pid, title, tags, account, name, u_id, user_link, img))
                con.commit()
                con.close()

            elif i_tpye == '擦边球':
                if os.path.exists('data/sqlite/setu/nearR18.db'):
                    print('数据文件存在！')
                else:
                    Text('数据库不存在，将在3秒后开始构建...')
                    time.sleep(3)
                    Text('开始构建数据库！')
                    con = sqlite3.connect(Path('.') / 'data' / 'sqlite' / 'setu' / 'nearR18.db')
                    cur = con.cursor()
                    cur.execute('CREATE TABLE nearR18(pid PID, title TITLE, tags TAGS, account ACCOUNT, name NAME, u_id UID, user_link USERLINK, img IMG, UNIQUE(pid, title, tags, account, name, u_id, user_link, img))')
                    con.commit()
                    cur.close()
                    con.close()
                    Text('完成')
    
                con = sqlite3.connect(Path('.') / 'data' / 'sqlite' / 'setu' / 'nearR18.db')
                cur = con.cursor()
                cur.execute('INSERT INTO nearR18 VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")'%(pid, title, tags, account, name, u_id, user_link, img))
                con.commit()
                con.close()

            elif i_tpye == 'r18':
                if os.path.exists('data/sqlite/cloudmusic/cloudmusic.db'):
                    print('数据文件存在！')
                else:
                    Text('数据库不存在，将在3秒后开始构建...')
                    time.sleep(3)
                    Text('开始构建数据库！')
                    con = sqlite3.connect(Path('.') / 'data' / 'sqlite' / 'setu' / 'r18.db')
                    cur = con.cursor()
                    cur.execute('CREATE TABLE r18(pid PID, title TITLE, tags TAGS, account ACCOUNT, name NAME, u_id UID, user_link USERLINK, img IMG, UNIQUE(pid, title, tags, account, name, u_id, user_link, img))')
                    con.commit()
                    cur.close()
                    con.close()
                    Text('完成')

                con = sqlite3.connect(Path('.') / 'data' / 'sqlite' / 'setu' / 'r18.db')
                cur = con.cursor()
                cur.execute('INSERT INTO r18 VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")'%(pid, title, tags, account, name, u_id, user_link, img))
                con.commit()
                con.close()
            
            end = time.perf_counter()
            
            Text(f'数据上传完成！\n耗时: {round(end - start, 3)}s')
        else:
            Text('抱歉哦，ATRI只听取主人的专属指令呢')

@deco.not_botself
def receive_group_msg(ctx: GroupMsg):
    msg = ctx.Content
    if re.findall(r"(上传[网易云|网抑云])", msg):
        if ctx.FromUserId == master:
            start = time.perf_counter()
            msg = msg.split(' ', 1)
            msg = msg[1]

            if os.path.exists('data/sqlite/cloudmusic/cloudmusic.db'):
                    print('数据文件存在！')
            else:
                Text('数据库不存在，将在3秒后开始构建...')
                time.sleep(3)
                Text('开始构建数据库！')
                con = sqlite3.connect(Path('.') / 'data' / 'sqlite' / 'cloudmusic' / 'cloudmusic.db')
                cur = con.cursor()
                cur.execute('CREATE TABLE cloudmusic(msg MSG, UNIQUE(msg))')
                con.commit()
                cur.close()
                con.close()
                Text('完成')
    
            con = sqlite3.connect(Path('.') / 'data' / 'sqlite' / 'cloudmusic' / 'cloudmusic.db')
            cur = con.cursor()
            cur.execute('INSERT INTO cloudmusic VALUES ("%s")'%(msg))
            con.commit()
            con.close()

            end = time.perf_counter()

            Text(f'数据上传完成！\n耗时: {round(end - start, 3)}s')
        
        else:
            Text(
                    choice(
                        [
                            '你我谁呢？？', '您配吗？', '恁哪位？', '仿生人是不会认错主人的！'
                        ]
                    )
                )


@deco.not_botself
def receive_group_msg(ctx: GroupMsg):
    msg = ctx.Content
    print(msg)
    if msg == '数据总量':
        con = sqlite3.connect(Path('.') / 'data' / 'sqlite' / 'setu' / 'normal.db') # setu-normal
        cur = con.cursor()
        cur.execute("select * from normal")
        data_normal = len(cur.fetchall())
        con.close()

        con = sqlite3.connect(Path('.') / 'data' / 'sqlite' / 'setu' / 'nearR18.db') # setu-nearR18
        cur = con.cursor()
        cur.execute("select * from nearR18")
        data_nearR18 = len(cur.fetchall())
        con.close()

        con = sqlite3.connect(Path('.') / 'data' / 'sqlite' / 'setu' / 'r18.db') # setu-r18
        cur = con.cursor()
        cur.execute("select * from r18")
        data_r18 = len(cur.fetchall())
        con.close()

        con = sqlite3.connect(Path('.') / 'data' / 'sqlite' / 'cloudmusic' / 'cloudmusic.db') # cloudmusic
        cur = con.cursor()
        cur.execute("select * from cloudmusic")
        data_cloudmusic = len(cur.fetchall())
        con.close()

        Action(ctx.CurrentQQ).send_group_text_msg(
            ctx.FromGroupId,
            content = f"目前螃蟹™数据库收录了：\n涩图：\n  normal: {data_normal}\n  nearR18: {data_nearR18}\n   r18：{data_r18}\n网抑云语录: {data_cloudmusic}"
        )