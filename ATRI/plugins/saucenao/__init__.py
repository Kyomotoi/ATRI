from re import findall
from random import choice

from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.adapters.cqhttp.message import Message, MessageSegment

from ATRI.config import SauceNAO
from ATRI.utils.limit import FreqLimiter
from .data_source import SaouceNao


_search_flmt = FreqLimiter(10)
_search_flmt_notice = choice(["慢...慢一..点❤", "冷静1下", "歇会歇会~~"])


saucenao = SaouceNao().on_command("以图搜图", "透过一张图搜索可能的来源")

@saucenao.args_parser  # type: ignore
async def _get_img(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    quit_list = ["算了", "罢了", "不搜了"]
    if msg in quit_list:
        await saucenao.finish("好吧...")
    if not msg:
        await saucenao.reject("图呢？")
    else:
        state["img"] = msg

@saucenao.handle()
async def _ready_search(bot: Bot, event: MessageEvent, state: T_State):
    user_id = event.get_user_id()
    if not _search_flmt.check(user_id):
        await saucenao.finish(_search_flmt_notice)
    
    msg = str(event.message).strip()
    if msg:
        state["img"] = msg

@saucenao.got("img", "图呢？")
async def _deal_search(bot: Bot, event: MessageEvent, state: T_State):
    user_id = event.get_user_id()
    msg = state["img"]
    img = findall(r"url=(.*?)]", msg)
    if not img:
        await saucenao.reject("请发送图片而不是其他东西！！")
    
    a = SaouceNao(SauceNAO.key)
    result = f"> {MessageSegment.at(user_id)}" + await a.search(img[0])
    _search_flmt.start_cd(user_id)
    await saucenao.finish(Message(result))
