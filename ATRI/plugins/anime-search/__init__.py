import re
import json

from nonebot.adapters.cqhttp.message import MessageSegment
from nonebot.plugin import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.adapters.cqhttp.message import Message
from nonebot.typing import T_State

from ATRI.rule import is_in_banlist, is_in_dormant
from ATRI.exceptions import RequestTimeOut
from ATRI.utils.request import get_bytes

from .data_source import to_simple_string


URL = "https://trace.moe/api/search?url="


anime_search = on_command(
    "/anime",
    rule=is_in_banlist() & is_in_dormant()
)

@anime_search.handle()
async def _anime_search(bot: Bot,
                        event: MessageEvent,
                        state: T_State) -> None:
    msg = str(event.message).strip()
    if msg:
        state["msg"] = msg

@anime_search.got("msg", prompt="请发送咱一张图片~！")
async def _(bot: Bot,
            event: MessageEvent,
            state: T_State) -> None:
    msg = state["msg"]
    img = re.findall(r"url=(.*?)]", msg)
    if not img:
        await anime_search.reject("请发送图片而不是其它东西！！")
    
    try:
        req = await get_bytes(URL + img[0])
    except RequestTimeOut:
        raise RequestTimeOut("Request failed!")
    
    data = json.loads(req)["docs"]
    try:
        d = {}
        for i in range(len(data)):
            if data[i]["title_chinese"] in d.keys():
                d[data[i]["title_chinese"]][0] += data[i]["similarity"]
            else:
                m = data[i]["at"] / 60
                s = data[i]["at"] % 60
                
                if not data[i]["episode"]:
                    n = 1
                else:
                    n = data[i]["episode"]
                
                d[to_simple_string(data[i]["title_chinese"])] = [
                    data[i]["similarity"],
                    f"第{n}集",
                    f"{int(m)}分{int(s)}秒处"
                ]
    except Exception as err:
        raise Exception(f"Invalid data.\n{err}")
    
    result = sorted(
        d.items(),
        key=lambda x:x[1],
        reverse=True
    )
    
    t = 0
    
    msg0 = f"{MessageSegment.at(event.user_id)}\nResult [{len(d)}]:"
    for i in result:
        t += 1
        s = "%.2f%%" % (i[1][0] * 100)
        msg0 = msg0 + (
            "\n——————————\n"
            f"({t}) Similarity: {s}\n"
            f"Name: {i[0]}\n"
            f"Time: {i[1][1]} {i[1][2]}"
        )
    
    await anime_search.finish(Message(msg0))
