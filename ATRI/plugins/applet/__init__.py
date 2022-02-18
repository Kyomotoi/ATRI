from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters.onebot.v11.helpers import Cooldown

from .data_source import Applet


bili_applet = Applet().on_message("b站小程序检测", "B站小程序爪巴", block=False)


@bili_applet.handle([Cooldown(3)])
async def _(event: MessageEvent):
    msg = str(event.get_message())
    try:
        result, is_ok = await Applet().msg_builder(msg)
    except Exception:
        return

    if not is_ok:
        return

    await bili_applet.finish(result)
