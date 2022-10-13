from random import choice

from nonebot.adapters.onebot.v11 import MessageEvent, Message, MessageSegment
from nonebot.adapters.onebot.v11.helpers import extract_image_urls, Cooldown

from ATRI.log import log
from ATRI.config import SauceNAO as sn
from ATRI.service import ServiceTools
from .data_source import SauceNao


_search_flmt_notice = choice(["慢...慢一..点❤", "冷静1下", "歇会歇会~~"])


saucenao = SauceNao().on_command("以图搜图", "透过一张图搜索可能的来源")


@saucenao.got("saucenao_img", "图呢？", [Cooldown(5, prompt=_search_flmt_notice)])
async def _deal_search(event: MessageEvent):

    # cache fix
    if not sn.key:
        ServiceTools.service_controller("以图搜图", False)
        log.warning("插件 SauceNao 所需的 key 未配置，将被全局禁用，后续填写请手动启用")

    user_id = event.get_user_id()
    img = extract_image_urls(event.message)
    if not img:
        await saucenao.reject("请发送图片而不是其他东西！！")

    try:
        a = SauceNao(sn.key)
    except Exception:
        await saucenao.finish("失败了...")

    result = f"> {MessageSegment.at(user_id)}" + await a.search(img[0])  # type: ignore
    await saucenao.finish(Message(result))
