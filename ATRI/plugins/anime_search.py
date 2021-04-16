import re
import json

from nonebot.adapters.cqhttp.message import MessageSegment
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.adapters.cqhttp.message import Message
from nonebot.typing import T_State

from ATRI.service import Service as sv
from ATRI.rule import is_in_service
from ATRI.exceptions import RequestTimeOut
from ATRI.utils.request import get_bytes
from ATRI.utils.translate import to_simple_string


URL = "https://trace.moe/api/search?url="


__doc__ = """
以图搜番
权限组：所有人
用法：
  以图搜番 (pic)
"""

anime_search = sv.on_command(
    cmd="以图搜番",
    docs=__doc__,
    rule=is_in_service('以图搜番')
)

@anime_search.args_parser  # type: ignore
async def _load_anime(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message)
    quit_list = ['算了', '罢了', '不搜了']
    if msg in quit_list:
        await anime_search.finish('好吧...')
    
    if not msg:
        await anime_search.reject('图呢？')
    else:
        state['pic_anime'] = msg

@anime_search.handle()
async def _anime_search(bot: Bot,
                        event: MessageEvent,
                        state: T_State) -> None:
    msg = str(event.message).strip()
    if msg:
        state['pic_anime'] = msg

@anime_search.got('pic_anime', prompt='图呢？')
async def _deal_search(bot: Bot,
            event: MessageEvent,
            state: T_State) -> None:
    msg = state['pic_anime']
    img = re.findall(r"url=(.*?)]", msg)
    if not img:
        await anime_search.reject("请发送图片而不是其它东西！！")
    
    try:
        req = await get_bytes(URL + img[0])
    except RequestTimeOut:
        raise RequestTimeOut("Request failed!")
    
    data = json.loads(req)["docs"]
    try:
        d = dict()
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
    
    msg0 = f"> {MessageSegment.at(event.user_id)}"
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
