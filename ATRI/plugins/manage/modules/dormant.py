from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import Bot, MessageEvent

from ATRI.service import Service as sv
from ATRI.rule import to_bot


__doc__ = """
休眠，不处理任何信息
权限组：维护者
用法：
  @ 休眠
"""

dormant_enabled = sv.on_command(
    cmd="休眠", docs=__doc__, rule=to_bot(), permission=SUPERUSER
)


@dormant_enabled.handle()
async def _dormant_enabled(bot: Bot, event: MessageEvent) -> None:
    sv.Dormant.control_dormant(True)
    msg = "已进入休眠状态...期间咱不会回应任何人的消息哦..."
    await dormant_enabled.finish(msg)


__doc__ = """
苏醒，开始处理信息
权限组：维护者
用法：
  @ 苏醒
"""

dormant_disabled = sv.on_command(
    cmd="苏醒", docs=__doc__, rule=to_bot(), permission=SUPERUSER
)


@dormant_disabled.handle()
async def _dormant_disabled(bot: Bot, event: MessageEvent) -> None:
    sv.Dormant.control_dormant(False)
    msg = "唔...早上好...——哇哈哈"
    await dormant_disabled.finish(msg)
