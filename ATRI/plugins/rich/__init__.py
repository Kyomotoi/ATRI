import re
import json
from random import choice
from aiohttp.client import ClientSession

from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.adapters.cqhttp.message import MessageSegment

from ATRI.service import Service as sv
from ATRI.utils.request import get_bytes
from ATRI.utils.limit import is_too_exciting

from .data_source import dec


temp_list = []
img_url = [
    "https://cdn.jsdelivr.net/gh/Kyomotoi/CDN@master/project/ATRI/fkrich.png",
    "https://cdn.jsdelivr.net/gh/Kyomotoi/CDN@master/project/ATRI/xixi.jpg",
]


bilibili_rich = sv.on_message()


@bilibili_rich.handle()
async def _bilibili_rich(bot: Bot, event: MessageEvent) -> None:
    global temp_list
    try:
        msg = str(event.raw_message).replace("\\", "")
        bv = False

        if "qqdocurl" not in msg:
            if "av" in msg:
                av = re.findall(r"(av\d+)", msg)[0].replace("av", "")
            else:
                bv = re.findall(r"(BV\w+)", msg)
                av = str(dec(bv[0]))
        else:
            patt = r"(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+"
            bv_url = re.findall(patt, msg)
            bv_url = bv_url[3]
            async with ClientSession() as session:
                async with session.get(url=bv_url) as r:
                    bv = re.findall(r"(BV\w+)", str(r.url))
                    av = dec(bv[0])

        if not bv:
            if "av" in msg:
                av = re.findall(r"(av\d+)", msg)[0].replace("av", "")
            else:
                return

        user = event.user_id
        check = is_too_exciting(user, 1, 10)
        if not check:
            return

        URL = f"https://api.kyomotoi.moe/api/bilibili/v2/?aid={av}"
        data = json.loads(await get_bytes(URL))["data"]
        repo = (
            f"{data['bvid']} INFO:\n"
            f"Title: {data['title']}\n"
            f"Link: {data['short_link']}\n"
            "にまねげぴのTencent rich!"
        )
        await bot.send(event, MessageSegment.image(file=choice(img_url)))
        await bilibili_rich.finish(repo)
    except BaseException:
        return
