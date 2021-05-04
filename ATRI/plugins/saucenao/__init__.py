import re
import json
from random import choice

from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.adapters.cqhttp.message import Message, MessageSegment
from nonebot.typing import T_State

from ATRI.config import SauceNAO
from ATRI.service import Service as sv
from ATRI.rule import is_in_service
from ATRI.exceptions import RequestError

from .data_source import SauceNao


__doc__ = """
以图搜图
权限组：所有人
用法：
  以图搜图 (pic)
"""

saucenao = sv.on_command(cmd="以图搜图", docs=__doc__, rule=is_in_service("以图搜图"))


@saucenao.args_parser  # type: ignore
async def _load_saucenao(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message)
    quit_list = ["算了", "罢了", "不搜了"]
    if msg in quit_list:
        await saucenao.finish("好吧...")

    if not msg:
        await saucenao.reject("图呢？")
    else:
        state["pic_sau"] = msg


@saucenao.handle()
async def _sauce_nao(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    if msg:
        state["pic_sau"] = msg


@saucenao.got("pic_sau", prompt="图呢？")
async def _deal_saucenao(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = state["pic_sau"]
    img = re.findall(r"url=(.*?)]", msg)
    if not img:
        await saucenao.finish("请发送图片而不是其他东西！！")

    try:
        task = SauceNao(api_key=SauceNAO.key)
        data = json.loads(await task.search(img[0]))
    except RequestError:
        raise RequestError("Request failed!")

    res = data["results"]
    result = list()
    for i in range(0, 3):
        data = res[i]

        _result = dict()
        _result["similarity"] = data["header"]["similarity"]
        _result["index_name"] = data["header"]["index_name"]
        _result["url"] = choice(data["data"].get("ext_urls", ["None"]))
        result.append(_result)

    msg0 = f"> {MessageSegment.at(event.user_id)}"
    for i in result:
        msg0 = msg0 + (
            "\n——————————\n"
            f"Similarity: {i['similarity']}\n"
            f"Name: {i['index_name']}\n"
            f"URL: {i['url'].replace('https://', '')}"
        )

    await saucenao.finish(Message(msg0))
