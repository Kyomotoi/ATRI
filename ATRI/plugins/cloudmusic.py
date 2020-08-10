# -*- coding:utf-8 -*-
import json
import nonebot
from orjson import loads
from html import unescape

from ATRI.modules import response # type: ignore

REPORT_FORMAT = """Status: {status}
Song id: {id}
Br: {br}
Download: {url}
MD5: {md5}"""


@nonebot.on_natural_language(only_to_me = False)
async def fk_tx_app_cloudmusic(session: nonebot.NLPSession):
    rich_message = [x for x in session.event['message'] if x.get('CQ') == 'rich']

    if not rich_message:
        return
    
    rich_message = rich_message[0]['data']
    print(rich_message)

    if '网易云音乐' not in str(rich_message):
        return
    
    if 'music' not in str(rich_message):
        return
    
    data = loads(unescape(rich_message))
    print(data
    )

    URL = data['music']['jumpUrl']
    rep = URL.split('/')
    wid = rep[4]

    url = f'https://api.imjad.cn/cloudmusic/?type=song&id={wid}&br=320000'
    print(url)

    dc = json.loads(response.request_api(url))

    await session.send(
        REPORT_FORMAT.format(
            status = dc["code"],
            id = dc["data"][0]["id"],
            br = dc["data"][0]["br"],
            url = dc["data"][0]["url"],
            md5 = dc["data"][0]["md5"],
        )
    )


@nonebot.on_natural_language(only_to_me = False)
async def cloudmusic_link(session: nonebot.NLPSession):
    share_message = [x for x in session.ctx['message'] if x.get('type') == 'share']
    
    if not share_message:
        return
    
    share_message = share_message[0]['data']['url']

    if 'music.163.com' not in str(share_message):
        return
    
    rep = share_message.replace('=', '/')
    rep = rep.replace('&', '/')
    wid = rep[4]

    url = f'https://api.imjad.cn/cloudmusic/?type=song&id={wid}&br=320000'
    print(url)

    dc = json.loads(response.request_api(url))

    await session.send(
        REPORT_FORMAT.format(
            status = dc["code"],
            id = dc["data"][0]["id"],
            br = dc["data"][0]["br"],
            url = dc["data"][0]["url"],
            md5 = dc["data"][0]["md5"],
        )
    )