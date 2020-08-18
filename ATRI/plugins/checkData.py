import json
import sqlite3
from pathlib import Path
from nonebot import on_command, CommandSession



@on_command('data_list', aliases = ['数据总量'], only_to_me = False)
async def _(session: CommandSession):
    user = session.event.user_id
    group = session.event.group_id
    try:
        with open(Path('.') / 'ATRI' / 'plugins' / 'noobList' / 'noobGroup.json', 'r') as f:
            data = json.load(f)
    except:
        data = {}
    
    try:
        with open(Path('.') / 'ATRI' / 'plugins' / 'noobList' / 'noobList.json', 'r') as f:
            data1 = json.load(f)
    except:
        data1 = {}

    if str(group) in data.keys():
        pass
    else:
        if str(user) in data1.keys():
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

            with open(Path('.') / 'ATRI' / 'plugins' / 'LearnRepo' / 'LearnRepo.json', 'r') as f:
                data = json.load(f)
            data_repo = len(data)

            await session.send(
                f"""目前螃蟹™数据库收录了：
    涩图：
        normal: {data_normal}
        nearR18: {data_nearR18}
        r18：{data_r18}
    网抑云语录：{data_cloudmusic}
    词汇量：{data_repo}"""
            )