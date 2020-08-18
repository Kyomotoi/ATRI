import json
import random
import nonebot
from datetime import datetime
from random import choice
from pathlib import Path
from nonebot import on_command, CommandSession
from nonebot.helpers import render_expression

import config # type: ignore


bot = nonebot.get_bot()
master = config.MASTER()


def now_time():
    now_ = datetime.now()
    hour = now_.hour
    minute = now_.minute
    now = hour + minute / 60
    return now


HELP_REPLY = (
    'ええと...让我想想...',
    '嗯...',
    '阿这',
    '不会使用嘛...ええと'
)


@on_command('抽签', only_to_me = False)
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
            if 0 <= now_time() < 5.5:
                await session.send(
                    choice(
                        [
                            'zzzz......',
                            'zzzzzzzz......',
                            'zzz...好涩哦..zzz....',
                            '别...不要..zzz..那..zzz..',
                            '嘻嘻..zzz..呐~..zzzz..'
                        ]
                    )
                )
            else:
                await session.send(
                    str(
                        random.choice(
                            [
                                '大凶',
                                '大胸',
                                '小凶',
                                '小胸',
                                '凶',
                                '吉',
                                '中吉',
                                '大吉',
                                '特大吉',
                                '超特大吉'
                            ]
                        )
                    )
                )

@on_command('掷骰子', aliases = ['扔骰子', '骰子'], only_to_me = False)
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
            if 0 <= now_time() < 5.5:
                await session.send(
                    choice(
                        [
                            'zzzz......',
                            'zzzzzzzz......',
                            'zzz...好涩哦..zzz....',
                            '别...不要..zzz..那..zzz..',
                            '嘻嘻..zzz..呐~..zzzz..'
                        ]
                    )
                )
            else:
                await session.send(
                    str(
                        random.randint(
                            1,6
                        )
                    )
                )

@on_command('关于', aliases = ['关于机器人'], only_to_me = False)
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
            if 0 <= now_time() < 5.5:
                await session.send(
                    choice(
                        [
                            'zzzz......',
                            'zzzzzzzz......',
                            'zzz...好涩哦..zzz....',
                            '别...不要..zzz..那..zzz..',
                            '嘻嘻..zzz..呐~..zzzz..'
                        ]
                    )
                )
            else:
                await session.send(
                    """想了解ATRI嘛
            写出咱的是Kyomotoi
            他的主页:https://blog.lolihub.icu/
            项目地址:https://github.com/Kyomotoi/ATRI
            欢迎star~w!"""
                )

@on_command('help', aliases = ['帮助', '如何使用ATRI', '机器人帮助'], only_to_me = False)
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
            if 0 <= now_time() < 5.5:
                await session.send(
                    choice(
                        [
                            'zzzz......',
                            'zzzzzzzz......',
                            'zzz...好涩哦..zzz....',
                            '别...不要..zzz..那..zzz..',
                            '嘻嘻..zzz..呐~..zzzz..'
                        ]
                    )
                )
            else:
                await session.send(
                    f"""{render_expression(HELP_REPLY)}
        请仔细阅读文档哦~~https://blog.lolihub.icu/#/ATRI/user"""
                )


@on_command('report', aliases = ['来杯红茶'], only_to_me = True)
async def _(session: CommandSession):
    h_type = session.event.detail_type
    msg = session.current_arg.strip()
    user = session.event.user_id
    group = session.event.group_id

    if not msg:
        msg = session.get('message', prompt='请键入需要反馈的信息')

    if h_type == 'group':
        await bot.send_private_msg(
            user_id = master,
            message = f"来自群[{group}]，用户[{user}]的反馈：\n{msg}"
        ) # type: ignore
    
    elif h_type == 'private':
        await bot.send_private_msg(
            user_id = master,
            message = f"来自用户[{user}]的反馈：\n{msg}"
        ) # type: ignore