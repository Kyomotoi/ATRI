from random import choice

from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters.onebot.v11.helpers import Cooldown

from ATRI.service import Service
from ATRI.permission import MASTER


_is_tietie = True
_tietie_wd = choice(
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

tt = Service("贴贴").document("全自动贴贴机").only_admin(True).permission(MASTER)


auto_tietie = tt.on_message(
    "贴贴w", "只与维护者贴贴w, '不可以贴'以拒绝贴贴~, '来贴贴'以接受贴贴~", block=False, priority=11
)


@auto_tietie.handle([Cooldown(600)])
async def _(event: MessageEvent):
    if not _is_tietie:
        await auto_tietie.finish()

    user_id = event.get_user_id()
    at = MessageSegment.at(user_id)
    result = at + _tietie_wd  # type: ignore
    await auto_tietie.finish(result)


no_tietie = tt.on_command("不可以贴", docs="拒绝贴贴")


@no_tietie.handle()
async def _():
    global _is_tietie
    _is_tietie = False
    await no_tietie.finish("好吧...")


yes_tietie = tt.on_command("来贴贴", docs="继续贴贴")


@yes_tietie.handle()
async def _():
    global _is_tietie
    _is_tietie = True
    await yes_tietie.finish("好欸！")
