from nonebot.typing import T_State
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import Bot, MessageEvent

from ATRI.service import Service as sv


__doc__ = """
紧急停机
权限组：维护者
用法：
  @ 关机
"""

shutdown = sv.on_command(cmd="关机", docs=__doc__, permission=SUPERUSER)


@shutdown.handle()
async def _shutdown(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    if msg:
        state["msg"] = msg


@shutdown.got("msg", prompt="[WARNING]此项操作将强行终止bot运行，是否继续(y/n)")
async def __shutdown(bot: Bot, event: MessageEvent, state: T_State) -> None:
    t = ["y", "Y", "是"]
    if state["msg"] in t:
        await bot.send(event, "咱还会醒来的，一定")
        exit(0)
    else:
        await shutdown.finish("再考虑下吧 ;w;")
