import json
from datetime import datetime
from random import choice
from nonebot import on_command, on_natural_language, CommandSession
from nonebot import NLPSession, NLPResult

from ATRI.modules.response import request_api
from ATRI.modules.error import errorBack
from ATRI.modules.funcControl import checkNoob


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
    if checkNoob(user, group):
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
            try:
                rep = request_api(url)
            except:
                session.finish(errorBack('请求错误'))
            
            dc = json.loads(rep)

            await session.send(dc["hitokoto"])

@on_natural_language('一言', only_to_me = False)
async def _(session: NLPSession):
    return NLPResult(60.0, ('hitokoto'), None)