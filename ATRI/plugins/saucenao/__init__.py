from random import choice

from nonebot.adapters.onebot.v11 import MessageEvent, Message, MessageSegment
from nonebot.adapters.onebot.v11.helpers import extract_image_urls, Cooldown

from ATRI.config import SauceNAO
from .data_source import SaouceNao


_search_flmt_notice = choice(["慢...慢一..点❤", "冷静1下", "歇会歇会~~"])


saucenao = SaouceNao().on_command("以图搜图", "透过一张图搜索可能的来源")


@saucenao.got("saucenao_img", "图呢？", [Cooldown(5, prompt=_search_flmt_notice)])
async def _deal_search(event: MessageEvent):
    user_id = event.get_user_id()
    img = extract_image_urls(event.message)
    if not img:
        await saucenao.reject("请发送图片而不是其他东西！！")

    try:
        a = SaouceNao(SauceNAO.key)
    except Exception:
        await saucenao.finish("失败了...")

    result = f"> {MessageSegment.at(user_id)}" + await a.search(img[0])  # type: ignore
    await saucenao.finish(Message(result))
