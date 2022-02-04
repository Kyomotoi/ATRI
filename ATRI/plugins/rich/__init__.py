from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.adapters.onebot.v11.helpers import Cooldown

from ATRI.log import logger as log
from .data_source import Rich


bili_rich = Rich().on_message("小程序检测", "小程序爪巴", block=False)


@bili_rich.handle([Cooldown(3)])
async def _fk_bili(event: MessageEvent):
    msg = str(event.message)
    try:
        result, is_ok = await Rich().fk_bili(msg)
    except Exception:
        return
    log.debug(result, is_ok)
    if not is_ok:
        return
    await bili_rich.finish(result)
