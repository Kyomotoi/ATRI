import json
from datetime import datetime
from random import choice
from pathlib import Path
from nonebot import on_command, on_natural_language, CommandSession
from nonebot import NLPSession, NLPResult

from ATRI.modules import response # type: ignore


def now_time():
    now_ = datetime.now()
    hour = now_.hour
    minute = now_.minute
    now = hour + minute / 60
    return now


url = 'https://api.imjad.cn/hitokoto/?cat=a&charset=utf-8&length=50&encode=json&fun=sync&source='


@on_command('hitokoto', aliases = ['一言'], only_to_me = False)
async def hitokoto(session: CommandSession):
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
                rep = response.request_api(url)
                
                if not rep:
                    session.finish('获取失败')
                
                dc = json.loads(response.request_api(url))

                await session.send(dc["hitokoto"])

@on_natural_language('一言', only_to_me = False)
async def _(session: NLPSession):
    return NLPResult(60.0, ('hitokoto'), None)