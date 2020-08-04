# -*- coding:utf-8 -*-
import time
import json
import nonebot
from nonebot import on_command, CommandSession
from nonebot import NLPSession
from nonebot.natural_language import NLPResult
from nonebot.plugin import on_natural_language

from ATRI.modules import response # type: ignore


bot = nonebot.get_bot()
master = bot.config.SUPERUSERS
apikey = bot.config.LOLICONAPI # type: ignore

URL = 'https://api.lolicon.app/setu/'

SETU_REPLY = """Title: {title}
Pid: {pid}
{setu}
---------------
完成时间:{time}s"""


@on_command('setu', aliases = ['图来', '涩图', '涩图来'], only_to_me = False)
async def setu(session: CommandSession):
    with open('ATRI/plugins/switch/switch.json', 'r') as f:
        data = json.load(f)

    if data["setu"] == 0:
        await session.send('别急！正在找图！')
        start = time.perf_counter()
        values = {
            "apikey": apikey,
            "r18": "0",
            "num": "1"
        }

        dc = json.loads(response.request_api_params(URL, values))
        end = time.perf_counter()

        await session.send(
            SETU_REPLY.format(
                title=dc["data"][0]["title"],
                pid=dc["data"][0]["pid"],
                setu=dc["data"][0]["url"],
                time = round(end - start, 3)
            )
        )

    else:
        await session.send('该功能已被禁用...')

@on_natural_language(['涩图', '色图'], only_to_me = False)
async def _(session: NLPSession):
    return NLPResult(60.0, ('setu'), None)