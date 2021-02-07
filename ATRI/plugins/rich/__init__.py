import re
import json
from aiohttp.client import ClientSession

from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.plugin import on_message

from ATRI.rule import is_in_banlist, is_in_dormant
from ATRI.utils.request import get_bytes
from .data_source import dec

bilibili_rich = on_message(
    rule=is_in_banlist() & is_in_dormant()
)

@bilibili_rich.handle()
async def _bilibili_rich(bot: Bot, event: MessageEvent) -> None:
    msg = str(event.raw_message)
    bv = False
    
    if "qqdocurl" not in msg:
        if "av" in msg:
            av = re.findall(r"(av\d+)", msg)[0].replace('av', '')
        else:
            try:
                bv = re.findall(r"(BV\w+)", msg)
                av = str(dec(bv[0]))
            except:
                return
    else:
        bv_url = re.findall(r"(..........b23...\S+\=)", msg)
        bv_url = bv_url[0].replace("\\", "")
        print(bv_url)
        async with ClientSession() as session:
            async with session.get(
                url=bv_url) as r:
                bv = re.findall(r"(BV\w+)", str(r.url))
                av = dec(bv[0])
    
    if not bv:
        if "av" in msg:
            av = re.findall(r"(av\d+)", msg)[0].replace('av', '')
        else:
            return
    
    try:
        URL = f"https://api.kyomotoi.moe/api/bilibili/v2/?aid={av}"
    except:
        return
    data = json.loads(await get_bytes(URL))['data']
    repo = (
        f"{av} INFO:\n"
        f"Title: {data['title']}\n"
        f"Bid: {data['bvid']}\n"
        f"View: {data['stat']['view']} Like: {data['stat']['like']}\n"
        f"Coin: {data['stat']['coin']} Share: {data['stat']['share']}\n"
        f"Link: {data['short_link']}\n"
        "にまねげぴのTencent rich!"
    )
    await bilibili_rich.finish(repo)
    