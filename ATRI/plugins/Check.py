import json
import time
import sqlite3
import psutil
from pathlib import Path
import nonebot
from nonebot import on_command, CommandSession

import config
from ATRI.modules.error import errorBack


bot = nonebot.get_bot()
master = config.SUPERUSERS
file = Path('.') / 'ATRI' / 'plugins' / 'noobList' / 'noobList.json'
file1 = Path('.') / 'ATRI' / 'plugins' / 'noobList' / 'noobGroup.json'


@on_command('data_list', aliases = ['数据总量'], only_to_me = False)
async def _(session: CommandSession):
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


@on_command('look_noobList', aliases = ['查看黑名单'], only_to_me = False)
async def _(session: CommandSession):
    start = time.perf_counter()
    try:
        with open(file, 'r') as f:
            data = json.load(f)
    except:
        data = {}

    try:
        with open(file1, 'r') as f:
            data0 = json.load(f)
    except:
        data0 = {}
    
    msg = f'被ATRI列入黑名单有以下列表：\n'
    try:
        msg1 = f'=====[用户]=====\n'
        msg += msg1
        for i in data.keys():
            msg0 = f'{i}\n'
            msg += msg0
    except:
        end = time.perf_counter()
        msg0 = f"==============\nDone time: {round(end - start, 3)}s"
        msg += msg0
        await session.send(msg)
        return

    try:
        msg1 = f'======[群]======\n'
        msg += msg1
        for i in data0.keys():
            msg0 = f'{i}\n'
            msg += msg0
    except:
        end = time.perf_counter()
        msg0 = f"==============\nDone time: {round(end - start, 3)}s"
        msg += msg0
        await session.send(msg)
        return

    end = time.perf_counter()
    msg0 = f"==============\nDone time: {round(end - start, 3)}s"
    msg += msg0
    await session.send(msg)


@on_command('look_power', aliases = ['查看权限组'], only_to_me = False)
async def _(session: CommandSession):
    start = time.perf_counter()
    try:
        with open(Path('.') / 'ATRI' / 'plugins' / 'UploadSqlite' / 'sepi.json', 'r') as f:
            data = json.load(f)
    except:
        data = {}

    try:
        with open(Path('.') / 'ATRI' / 'plugins' / 'UploadSqlite' / 'cloudmusic.json', 'r') as f:
            data0 = json.load(f)
    except:
        data0 = {}
    
    msg = f'主人: {master}\n'
    try:
        msg1 = f'=====[涩批]=====\n'
        msg += msg1
        for i in data.keys():
            msg0 = f'{i}\n'
            msg += msg0
    except:
        end = time.perf_counter()
        msg0 = f"==============\nDone time: {round(end - start, 3)}s"
        msg += msg0
        await session.send(msg)
        return

    try:
        msg1 = f'====[网抑云]====\n'
        msg += msg1
        for i in data0.keys():
            msg0 = f'{i}\n'
            msg += msg0
    except:
        end = time.perf_counter()
        msg0 = f"==============\nDone time: {round(end - start, 3)}s"
        msg += msg0
        await session.send(msg)
        return

    end = time.perf_counter()
    msg0 = f"==============\nDone time: {round(end - start, 3)}s"
    msg += msg0
    await session.send(msg)



@on_command('check_status', patterns = [r"检查状态|检查运行|检查身体|查看状态"])
async def _(session: CommandSession):
    user = session.event.user_id
    group = session.event.group_id
    try:
        with open(file1, 'r') as f:
            data = json.load(f)
    except:
        data = {}
    
    try:
        with open(file, 'r') as f:
            data1 = json.load(f)
    except:
        data1 = {}

    if str(group) in data.keys():
        pass
    else:
        if str(user) in data1.keys():
            pass
        else:
            try:
                cpu = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory().percent
                disk = psutil.disk_usage('/').percent
                inteSENT = psutil.net_io_counters().bytes_sent # type: ignore
                inteRECV = psutil.net_io_counters().bytes_recv # type: ignore
            except:
                await session.send(errorBack('获取状态数据失败'))

            status = 'アトリは、高性能ですから！'

            if cpu > 80:
                status = 'ATRI感觉头有点晕...'
                if memory > 80:
                    status = 'ATRI感觉有点头晕并且有点累...'
            
            elif disk > 80:
                status = 'ATRI感觉身体要被塞满了...'

            await session.send(f"""ATRI Status：
* cpu: {cpu}%
* mem: {memory}%
* disk: {disk}%
* BytesSENT: {inteSENT}
* BytesRECV: {inteRECV}
{status}""".strip())

@on_command('getUser', aliases = ['用户总数', '用户数量'])
async def _(session: CommandSession):
    try:
        with open(Path('.') / 'ATRI' / 'modules' / 'favoIMP' / 'user.json', 'r') as f:
                data = json.load(f)
    except:
        data = {}
    msg0 = f'用户总数: {len(data)}\n'
    msg0 += f'群总数: {len(await session.bot.get_group_list())}' # type: ignore
    await session.send(msg0)



@on_command('trackERROR', aliases = ['track'], only_to_me = False)
async def _(session: CommandSession):
    if session.event.user_id in master:
        msg = session.current_arg.strip()
        if not msg:
            msg = session.get('message', prompt = '请发送trackID')

        try:
            with open(Path('.') / 'ATRI' / 'data' / 'errorData' / 'errorData.json', 'r') as f:
                data = json.load(f)
        except:
            data = {}

        if str(msg) in data.keys():
            err = data[f"{msg}"]
            msg0 = f'trackID: {msg}\n'
            msg0 += err
            await session.send(msg0)

        else:
            session.finish('未发现该ID')
    
    else:
        await session.send('恁哪位呀~？')