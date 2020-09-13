import os
import nonebot
from pathlib import Path
from random import choice, randint
from datetime import datetime
from nonebot import on_command, CommandSession

from ATRI.modules.error import errorBack
from ATRI.modules.funcControl import checkNoob


bot = nonebot.get_bot()


def now_time():
    now_ = datetime.now()
    hour = now_.hour
    minute = now_.minute
    now = hour + minute / 60
    return now


@on_command('nanjya', patterns = [r"なんじゃ|何[がで]|どうして|为什么|为何|多[洗西]跌"], only_to_me = False)
async def _(session: CommandSession):
    user = session.event.user_id
    group = session.event.group_id
    if checkNoob(user, group):
        if 0 <= now_time() < 5.5:
            pass
        else:
            if randint(1,2) == 1:
                img = choice(
                    [
                        '1.jpg', '8.jpg', '14.jpg', '21.jpg'
                    ]
                )
                img = os.path.abspath(Path('.') / 'ATRI' / 'data' / 'emoji' / 'senren' / f'{img}')
                await session.send(f'[CQ:image,file=file:///{img}]')

@on_command('wenhao', patterns = [r"'?'|？|¿"], only_to_me = False)
async def _(session: CommandSession):
    user = session.event.user_id
    group = session.event.group_id
    if checkNoob(user, group):
        if 0 <= now_time() < 5.5:
            pass
        else:
            if randint(1,3) == 1:
                res = randint(1,5)
                if 1 <= res < 2:
                    await session.send(
                        choice(
                            [
                                '?', '？', '嗯？', '(。´・ω・)ん?', 'ん？'
                            ]
                        )
                    )
                
                elif 2 <= res <= 5:
                    img = choice(
                        [
                            'WH.jpg', 'WH1.jpg', 'WH2.jpg', 'WH3.jpg', 'WH4.jpg'
                        ]
                    )
                    img = Path('.') / 'ATRI' / 'data' / 'emoji' / f'{img}'
                    img = os.path.abspath(img)
                    await session.send(f'[CQ:image,file=file:///{img}]')

@on_command('yesorno', patterns = [r"[好是]吗|[行能]不[行能]|彳亍不彳亍|可不可以"], only_to_me = False)
async def _(session: CommandSession):
    user = session.event.user_id
    group = session.event.group_id
    if checkNoob(user, group):
        if 0 <= now_time() < 5.5:
            pass
        else:
            res = randint(1,2)
            if res == 1:
                img = choice(
                    [
                        '2.png', '39.png'
                    ]
                )
                img = os.path.abspath(Path('.') / 'ATRI' / 'data' / 'emoji' / 'senren' / f'{img}')
                await session.send(f'[CQ:image,file=file:///{img}]')

            elif res == 2:
                img = choice(
                    [
                        'YIQI_YES.png', 'YIQI_NO.jpg', 'KD.jpg', 'FD.jpg'
                    ]
                )
                img = os.path.abspath(Path('.') / 'ATRI' / 'data' / 'emoji' / f'{img}')
                await session.send(f'[CQ:image,file=file:///{img}]')

@on_command('ysdd', aliases = [r"原声大碟"])
async def _(session: CommandSession):
    user = session.event.user_id
    group = session.event.group_id
    if checkNoob(user, group):
        try:
            voice = Path('.') / 'ATRI' / 'data' / 'voice' / 'ysdd.amr'
            voice = os.path.abspath(voice)
            await session.send(f'[CQ:record,file=file:///{voice}]')
        except:
            session.finish(errorBack('读取音频时出错'))