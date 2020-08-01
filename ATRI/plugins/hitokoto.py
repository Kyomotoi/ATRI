# -*- coding:utf-8 -*-
import json
from nonebot import on_command, on_natural_language, CommandSession
from nonebot import NLPSession, NLPResult
from ATRI.modules import response


url = f'https://api.imjad.cn/hitokoto/?cat=a&charset=utf-8&length=50&encode=json&fun=sync&source='


HITOKOTO_REPLY = """{hitokoto}
                from {author}"""


@on_command('hitokoto', aliases = ['一言'], only_to_me = False)
async def hitokoto(session: CommandSession):
    rep = response.request_api(url)
    
    if not rep:
        session.finish('获取失败')
    
    dc = json.loads(response.request_api(url))

    await session.send(
        HITOKOTO_REPLY.format(
            hitokoto = dc["hitokoto"],
            author = dc["author"]
        )
    )

@on_natural_language('一言', only_to_me = False)
async def _(session: NLPSession):
    return NLPResult(60.0, ('hitokoto',), None)