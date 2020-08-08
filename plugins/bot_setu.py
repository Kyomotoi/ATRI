import re
import json
import time
from pathlib import Path
from random import randint
from iotbot.action import Action
from iotbot import GroupMsg
from iotbot import decorators as deco
from iotbot.sugar import Text

from tools import response #type: ignore
import config_ #type: ignore


master = config_.MASTER()
apikey = config_.LOLICONAPI()

URL = 'https://api.lolicon.app/setu/'


@deco.not_botself
def receive_group_msg(ctx: GroupMsg):
    msg = ctx.Content
    group = ctx.FromGroupId

    if re.findall(r"来[点丶1一张份一副][涩色瑟][图圖]|[涩色瑟][图圖]来|[涩色瑟][图圖][gkdGKD搞快点]|[图圖]来|[我你她他它]想要[点丶1一张份一副][涩色瑟]", msg):
        with open(Path('.') / 'data' / 'switch' / 'switch.json', 'r') as f:
            data = json.load(f)
        
        if data["setu"] == 0:
            Text('别急！正在找图！')
            start = time.perf_counter()
            values = {
                "apikey": apikey,
                "r18": "0",
                "num": "1"
            }

            dc = json.loads(response.request_api_params(URL, values))
            end = time.perf_counter()

            title = dc["data"][0]["title"]
            pid = dc["data"][0]["pid"]

            res = randint(1,3)
            if 1 <= res <= 2: 
                Action(ctx.CurrentQQ).send_group_pic_msg(
                    ctx.FromGroupId,
                    picUrl = dc["data"][0]["url"],
                    content = f"Title: {title}\nPid: {pid}\n完成时间: {round(end - start, 3)}"
                )
            elif 2 < res <= 3:
                Action(ctx.CurrentQQ).send_group_text_msg(
                    ctx.FromGroupId,
                    conten = "我找到涩图了！但我发给主人了ο(=•ω＜=)ρ⌒☆"
                )
                time.sleep(1)
                Action(ctx.CurrentQQ).send_friend_pic_msg(
                    toUser = master,
                    picUrl = dc["data"][0]["url"],
                    content = f"主人，从群{group}来的涩图！热乎着！\nTitle: {title}\nPid: {pid}\n完成时间: {round(end - start, 3)}"
                )

        else:
            Text('该功能已被禁用...')