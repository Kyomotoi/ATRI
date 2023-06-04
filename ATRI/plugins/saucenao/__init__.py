from random import choice

from nonebot.adapters.onebot.v11 import MessageEvent, Message, MessageSegment
from nonebot.adapters.onebot.v11.helpers import Cooldown, extract_image_urls

from ATRI import conf
from ATRI.log import log
from ATRI.service import Service, ServiceTools

from .data_source import SauceNAO


plugin = Service("以图搜图").document("以图搜图，仅限二刺螈")


_search_flmt_notice = choice(["慢...慢一..点❤", "冷静1下", "歇会歇会~~"])


search = plugin.on_command("以图搜图", "透过一张图搜索可能的来源")


@search.got("img", "图呢？", [Cooldown(5, prompt=_search_flmt_notice)])
async def _do_search(event: MessageEvent):
    if not conf.SauceNAO.key:
        ServiceTools("以图搜图").service_controller(False)
        log.warning("插件 以图搜图 所需的 key (SauceNAO) 未配置，将被全局禁用，后续填写请手动启用")

    user_id = event.get_user_id()
    img = extract_image_urls(event.get_message())
    if not img:
        await search.reject("请发送图片而不是其他东西！！")

    try:
        result = await SauceNAO(conf.SauceNAO.key).search(img[0])
    except Exception as err:
        await search.finish(f"搜索失败：{str(err)}")

    await search.finish(Message(f"> {MessageSegment.at(user_id)}\n" + result))
