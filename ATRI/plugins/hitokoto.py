import json
from nonebot import on_command, on_natural_language, CommandSession
from nonebot import NLPSession, NLPResult

from ATRI.modules.response import request_api
from ATRI.modules.error import errorBack
from ATRI.modules.time import sleepTime
from ATRI.modules.funcControl import checkNoob



url = 'https://api.imjad.cn/hitokoto/?cat=a&charset=utf-8&length=50&encode=json&fun=sync&source='


@on_command('hitokoto', aliases = ['一言'], only_to_me = False)
async def hitokoto(session: CommandSession):
    user = session.event.user_id
    group = session.event.group_id
    if checkNoob(user, group):
        if sleepTime():
            await session.send(sleepTime())
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