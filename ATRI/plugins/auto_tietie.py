from random import choice

from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters.onebot.v11.helpers import Cooldown

from ATRI.service import Service
from ATRI.permission import MASTER


__TIETIE_ENABLED = True
__TIETIE_WORDS = choice(
    [
        "mua!",
        "贴贴!",
        MessageSegment.image(
            file="https://jsd.imki.moe/gh/Kyomotoi/CDN@master/project/ATRI/wife0.jpg"
        ),
        MessageSegment.image(
            file="https://jsd.imki.moe/gh/Kyomotoi/CDN@master/project/ATRI/wife1.jpg"
        ),
        MessageSegment.image(
            file="https://jsd.imki.moe/gh/Kyomotoi/CDN@master/project/ATRI/wife2.jpg"
        ),
        MessageSegment.image(
            file="https://jsd.imki.moe/gh/Kyomotoi/CDN@master/project/ATRI/wife3.jpg"
        ),
    ]
)

plugin = Service("贴贴").document("全自动贴贴机").permission(MASTER)


auto_tietie = plugin.on_message(
    "贴贴w", "只与维护者贴贴w, '不可以贴'以拒绝贴贴~, '来贴贴'以接受贴贴~", block=False, priority=11
)


@auto_tietie.handle([Cooldown(600)])
async def _(event: MessageEvent):
    if not __TIETIE_ENABLED:
        await auto_tietie.finish()

    user_id = event.get_user_id()
    at = MessageSegment.at(user_id)
    result = at + __TIETIE_WORDS  # type: ignore
    await auto_tietie.finish(result)


no_tietie = plugin.on_command("不可以贴", docs="拒绝贴贴")


@no_tietie.handle()
async def _():
    global __TIETIE_ENABLED
    __TIETIE_ENABLED = False
    await no_tietie.finish("好吧...")


yes_tietie = plugin.on_command("来贴贴", docs="继续贴贴")


@yes_tietie.handle()
async def _():
    global __TIETIE_ENABLED
    __TIETIE_ENABLED = True
    await yes_tietie.finish("好欸！")
