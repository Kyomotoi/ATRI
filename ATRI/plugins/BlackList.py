import time
import json
from pathlib import Path
from nonebot import on_command, CommandSession

import config # type: ignore


master = config.MASTER()


@on_command('add_noobList', aliases = ['屏蔽', '移除'], only_to_me = False)
async def _(session: CommandSession):
    if session.event.user_id == master:
        msg = session.event.raw_message.split(' ', 1)
        b_type = msg[0]
        user = msg[1]

        if b_type == '屏蔽':
            bL = {}
            bL[f"{user}"] = f"{user}"
            file = Path('.') / 'ATRI' / 'plugins' / 'noobList' / 'noobList.json'
            f = open(file, 'w')
            f.write(json.dumps(bL))
            f.close()
            await session.send(f'正义执行！！[{user}]已被ATRI屏蔽！')
        
        elif b_type == '移除':
            file = Path('.') / 'ATRI' / 'plugins' / 'noobList' / 'noobList.json'
            with open(file, 'r') as f:
                bL = json.load(f)
            bL.pop(f"{user}")
            f = open(file, 'w')
            f.write(json.dumps(bL))
            f.close()
            await session.send('将[{user}]移出黑名单成功~！')


@on_command('look_noobList', aliases = ['查看黑名单'], only_to_me = False)
async def _(session: CommandSession):
    start = time.perf_counter()
    with open('ATRI/plugins/noobList/noobList.json', 'r') as f:
        data = json.load(f)
    
    msg = f'被ATRI列入黑名单有以下账号：\n=============\n'
    for i in data.keys():
        msg0 = f'{i}\n'
        msg += msg0
    end = time.perf_counter()
    msg0 = f"=============\nDone time: {round(end - start, 3)}s"
    msg += msg0
    await session.send(msg)
