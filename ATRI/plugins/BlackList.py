import time
import json
from pathlib import Path
from nonebot import on_command, CommandSession

import config # type: ignore


master = config.MASTER()
file = Path('.') / 'ATRI' / 'plugins' / 'noobList' / 'noobList.json'
file1 = Path('.') / 'ATRI' / 'plugins' / 'noobList' / 'noobGroup.json'


@on_command('add_noobList', aliases = ['屏蔽', '移除'], only_to_me = False)
async def _(session: CommandSession):
    if session.event.user_id == master:
        msg = session.event.raw_message.split(' ', 2)
        b_type = msg[0]
        g_type = msg[1]
        u = msg[2]

        if g_type == 'qq':
            if b_type == '屏蔽':
                try:
                    with open(file, 'r') as f:
                        bL = json.load(f)
                except:
                    bL = {}
                bL[f"{u}"] = f"{u}"
                f = open(file, 'w')
                f.write(json.dumps(bL))
                f.close()
                await session.send(f'正义执行！！[{u}]已被ATRI屏蔽！')
            
            elif b_type == '移除':
                try:
                    with open(file, 'r') as f:
                        bL = json.load(f)
                except:
                    bL = {}
                bL.pop(f"{u}")
                f = open(file, 'w')
                f.write(json.dumps(bL))
                f.close()
                await session.send(f'将[{u}]移出黑名单成功~！')
        
        elif g_type == 'group':
            if b_type == '屏蔽':
                try:
                    with open(file1, 'r') as f:
                        bL = json.load(f)
                except:
                    bL = {}
                bL[f"{u}"] = f"{u}"
                f = open(file1, 'w')
                f.write(json.dumps(bL))
                f.close()
                await session.send(f'正义执行！！群[{u}]已被ATRI屏蔽！') 
            
            elif b_type == '移除':
                try:
                    with open(file1, 'r') as f:
                        bL = json.load(f)
                except:
                    bL = {}
                bL.pop(f"{u}")
                f = open(file1, 'w')
                f.write(json.dumps(bL))
                f.close()
                await session.send(f'将群[{u}]移出黑名单成功~！')


@on_command('look_noobList', aliases = ['查看黑名单'], only_to_me = False)
async def _(session: CommandSession):
    start = time.perf_counter()
    with open(file, 'r') as f:
        data = json.load(f)
    with open(file1, 'r') as f:
        data0 = json.load(f)
    
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