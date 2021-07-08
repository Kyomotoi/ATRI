from nonebot.adapters.cqhttp import Bot, MessageEvent

from ATRI.utils.limit import FreqLimiter
from .data_source import Rich


_rich_flmt = FreqLimiter(2)


bili_rich = Rich().on_message("小程序爪巴", block=False)

@bili_rich.handle()
async def _fk_bili(bot: Bot, event: MessageEvent):
    user_id = event.get_user_id()
    if not _rich_flmt.check(user_id):
        return
    
    msg = str(event.message)
    try:
        result, is_ok = await Rich().fk_bili(msg)
    except BaseException:
        return
    if not is_ok:
        return
    _rich_flmt.start_cd(user_id)
    await bili_rich.finish(result)
