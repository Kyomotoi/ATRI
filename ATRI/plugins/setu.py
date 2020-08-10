# -*- coding:utf-8 -*-
import os
import time
import json
from random import choice, randint
from pathlib import Path
import nonebot
from nonebot import on_command, CommandSession
from nonebot import MessageSegment

import config # type: ignore
from ATRI.modules import response # type: ignore


bot = nonebot.get_bot()
master = config.MASTER()
apikey = bot.config.LOLICONAPI # type: ignore

URL = 'https://api.lolicon.app/setu/'

SETU_REPLY = """Title: {title}
Pid: {pid}
{setu}
---------------
Complete time:{time}s"""


@on_command('setu', patterns = (r"来[点丶张份副个幅][涩色瑟][图圖]|[涩色瑟][图圖]来|[涩色瑟][图圖][gkd|GKD|搞快点]|[gkd|GKD|搞快点][涩色瑟][图圖]|[图圖]来|[我你她他它]想要[点丶张份副][涩色瑟][图圖]|我想要[1一][张份幅副个只][涩色瑟][图圖]|[我你她他它]想[看|look][涩涩|色色]的东西"), only_to_me = False)
async def setu(session: CommandSession):
    group = session.event.group_id
    with open(Path('.') / 'ATRI' / 'plugins' / 'switch' / 'switch.json', 'r') as f:
        data = json.load(f)

    if data["setu"] == 0:
        await session.send('别急！正在找图！')
        start = time.perf_counter()
        values = {
            "apikey": apikey,
            "r18": "0",
            "num": "1"
        }

        res = randint(1,10)
        if 1 <= res <= 9:
            res = randint(1,4)
            if 1 <= res <= 3:
                try:
                    dc = json.loads(response.request_api_params(URL, values))
                    title = dc["data"][0]["title"]
                    pid = dc["data"][0]["pid"]
                    setu = dc["data"][0]["url"] #b64.b64_str_img_url(dc["data"][0]["url"])
                except:
                    await session.send('失败了失败了失败了失...')
                    return
                

                res = randint(1,3)
                if 1 <= res <= 2:
                    end = time.perf_counter()
                    await session.send(
                        SETU_REPLY.format(
                        title = title,
                        pid = pid,
                        setu = dc["data"][0]["url"],
                        time = round(end - start, 3)
                        )
                    )
                
                elif res == 3:
                    await session.send('我找到涩图了！但我发给主人了ο(=•ω＜=)ρ⌒☆')
                    end = time.perf_counter()
                    await bot.send_private_msg( # type: ignore
                        user_id = master,
                        message = f"主人，从群{group}来的涩图！热乎着！\nTitle: {title}\nPid: {pid}\n{setu}\nComplete time: {round(end - start, 3)}"
                    )
            
            elif res == 4:
                img = choice(
                    [
                        'SP.jpg', 'SP1.jpg', 'SP2.jpg'
                    ]
                )
                img = Path('.') / 'ATRI' / 'data' / 'emoji' / f'{img}'
                img = os.path.abspath(img)
                await session.send(f'[CQ:image,file=file:///{img}]')

        
        elif res == 10:
            img = choice(
                [
                    'GDZ.png', 'SHZY1.jpg', 'SHZY2.jpg', 'SHZY3.jpg', 'SHZY4.jpg', 'SHZY5.jpg', 'SHZY6.jpg'
                ]
            )
            img = Path('.') / 'ATRI' / 'data' / 'img' / 'niceIMG' / f'{img}'
            await session.send(f'[CQ:image,file=file:///{img}]')

    else:
        await session.send('该功能已被禁用...')