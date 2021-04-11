import re
import json
from aiohttp.client import ClientSession
from nonebot.adapters.cqhttp import Bot, MessageEvent

from ATRI.service import Service as sv
from ATRI.utils.request import get_bytes
from ATRI.utils.list import count_list, del_list_aim

from .data_source import dec


temp_list = []


bilibili_rich = sv.on_message()

@bilibili_rich.handle()
async def _bilibili_rich(bot: Bot, event: MessageEvent) -> None:
    global temp_list
    msg = str(event.raw_message).replace("\\", "")
    bv = False
    
    if "qqdocurl" not in msg:
        if "av" in msg:
            try:
                av = re.findall(r"(av\d+)", msg)[0].replace('av', '')
            except:
                return
        else:
            try:
                bv = re.findall(r"(BV\w+)", msg)
                av = str(dec(bv[0]))
            except:
                return
    else:
        patt = r"(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+"
        bv_url = re.findall(patt, msg)
        bv_url = bv_url[3]
        async with ClientSession() as session:
            async with session.get(
                url=bv_url) as r:
                bv = re.findall(r"(BV\w+)", str(r.url))
                av = dec(bv[0])
    
    if not bv:
        if "av" in msg:
            try:
                av = re.findall(r"(av\d+)", msg)[0].replace('av', '')
            except:
                return
        else:
            return
    
    if count_list(temp_list, av) == 4:
        await bot.send(event, "你是怕别人看不到么发这么多次？")
        temp_list = del_list_aim(temp_list, av)
        return
    
    temp_list.append(av)
    
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
