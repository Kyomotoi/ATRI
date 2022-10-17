from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters.onebot.v11.helpers import Cooldown

from ATRI.service import Service

from .data_source import Applet


plugin = Service("小程序处理").document("啥b腾讯小程序给👴爪巴\n目前只整了b站的")


bili_applet = plugin.on_message("b站小程序检测", "B站小程序爪巴", priority=5, block=False)


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
