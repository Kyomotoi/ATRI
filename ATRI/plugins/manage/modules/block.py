from nonebot.typing import T_State
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import Bot, MessageEvent

from ATRI.service import Service as sv


__doc__ = """
封禁用户
权限组：维护者
用法：
  封禁用户 QQ号
"""

block_user = sv.on_command(cmd="封禁用户", docs=__doc__, permission=SUPERUSER)


@block_user.args_parser  # type: ignore
async def _block_user_load(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    cancel = ["算了", "罢了"]
    if msg in cancel:
        await block_user.finish("好吧...")
    if not msg:
        await block_user.reject("是谁呢？！GKD！")
    else:
        state["noob"] = msg


@block_user.handle()
async def _block_user(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    if msg:
        state["noob"] = msg


@block_user.got("noob", prompt="是谁呢？！GKD！")
async def _deal_block_user(bot: Bot, event: MessageEvent, state: T_State) -> None:
    noob = state["noob"]
    sv.BlockSystem.control_list(True, user=noob)
    msg = f"用户[{noob}]已被封禁(；′⌒`)"
    await block_user.finish(msg)


__doc__ = """
解封用户
权限组：维护者
用法：
  解封用户 QQ号
"""

unblock_user = sv.on_command(cmd="解封用户", docs=__doc__, permission=SUPERUSER)


@unblock_user.args_parser  # type: ignore
async def _unblock_user_load(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    cancel = ["算了", "罢了"]
    if msg in cancel:
        await unblock_user.finish("好吧...")
    if not msg:
        await unblock_user.reject("要原谅谁呢...")
    else:
        state["forgive"] = msg


@unblock_user.handle()
async def _unblock_user(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    if msg:
        state["forgive"] = msg


@unblock_user.got("forgive", prompt="要原谅谁呢...")
async def _deal_unblock_user(bot: Bot, event: MessageEvent, state: T_State) -> None:
    forgive = state["forgive"]
    sv.BlockSystem.control_list(False, user=forgive)
    msg = f"用户[{forgive}]已被解封ヾ(´･ω･｀)ﾉ"
    await unblock_user.finish(msg)


__doc__ = """
封禁群
权限组：维护者
用法：
  封禁群 群号
"""

block_group = sv.on_command(cmd="封禁群", docs=__doc__, permission=SUPERUSER)


@block_group.args_parser  # type: ignore
async def _block_group_load(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    cancel = ["算了", "罢了"]
    if msg in cancel:
        await block_user.finish("好吧...")
    if not msg:
        await block_user.reject("是哪个群？！GKD！")
    else:
        state["noob_g"] = msg


@block_group.handle()
async def _block_group(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    if msg:
        state["noob_g"] = msg


@block_group.got("noob_g", prompt="是哪个群？！GKD！")
async def _deal_block_group(bot: Bot, event: MessageEvent, state: T_State) -> None:
    noob_g = state["noob_g"]
    sv.BlockSystem.control_list(True, group=noob_g)
    msg = f"群[{noob_g}]已被封禁(；′⌒`)"
    await block_user.finish(msg)


__doc__ = """
解封群
权限组：维护者
用法：
  解封 群号
"""

unblock_group = sv.on_command(cmd="解封群", docs=__doc__, permission=SUPERUSER)


@unblock_group.args_parser  # type: ignore
async def _unblock_group_load(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    cancel = ["算了", "罢了"]
    if msg in cancel:
        await block_user.finish("好吧...")
    if not msg:
        await block_user.reject("要原谅哪个群呢...")
    else:
        state["forgive_g"] = msg


@unblock_group.handle()
async def _unblock_group(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    if msg:
        state["forgive_g"] = msg


@unblock_group.got("forgive_g", prompt="要原谅哪个群呢...")
async def _deal_unblock_group(bot: Bot, event: MessageEvent, state: T_State) -> None:
    forgive_g = state["forgive_g"]
    sv.BlockSystem.control_list(False, group=forgive_g)
    msg = f"群[{forgive_g}]已被解封ヾ(´･ω･｀)ﾉ"
    await unblock_user.finish(msg)
