from re import findall
from random import choice

from nonebot.matcher import Matcher
from nonebot.params import ArgPlainText, CommandArg
from nonebot.adapters.onebot.v11 import MessageEvent, Message, MessageSegment

from ATRI.config import SauceNAO
from ATRI.utils.limit import FreqLimiter
from .data_source import SaouceNao


_search_flmt = FreqLimiter(10)
_search_flmt_notice = choice(["慢...慢一..点❤", "冷静1下", "歇会歇会~~"])


saucenao = SaouceNao().on_command("以图搜图", "透过一张图搜索可能的来源")


@saucenao.handle()
async def _ready_search(
    matcher: Matcher, event: MessageEvent, args: Message = CommandArg()
):
    user_id = event.get_user_id()
    if not _search_flmt.check(user_id):
        await saucenao.finish(_search_flmt_notice)

    msg = args.extract_plain_text()
    if msg:
        matcher.set_arg("saucenao_img", args)


@saucenao.got("saucenao_img", "图呢？")
async def _deal_search(event: MessageEvent, msg: str = ArgPlainText("saucenao_img")):
    user_id = event.get_user_id()
    img = findall(r"url=(.*?)]", msg)
    if not img:
        await saucenao.reject("请发送图片而不是其他东西！！")

    try:
        a = SaouceNao(SauceNAO.key)
    except Exception:
        await saucenao.finish("失败了...")

    result = f"> {MessageSegment.at(user_id)}" + await a.search(img[0])  # type: ignore
    _search_flmt.start_cd(user_id)
    await saucenao.finish(Message(result))
