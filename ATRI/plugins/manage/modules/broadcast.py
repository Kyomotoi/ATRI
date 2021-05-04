import asyncio
from random import randint

from nonebot.typing import T_State
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import Bot, MessageEvent

from ATRI.service import Service as sv


__doc__ = """
群发内容
权限组：维护者
用法：
  广播 内容
"""

broadcast = sv.on_command(cmd="广播", docs=__doc__, permission=SUPERUSER)


@broadcast.args_parser  # type: ignore
async def _broadcast_load(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message)
    quit_list = ["算了", "罢了", "取消"]
    if msg in quit_list:
        await broadcast.finish("好吧...")
    if not msg:
        await broadcast.reject("想群发啥呢0w0")
    else:
        state["msg"] = msg


@broadcast.handle()
async def _broadcast(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    if msg:
        state["msg"] = msg


@broadcast.got("msg", prompt="请告诉咱需要群发的内容~！")
async def _deal_broadcast(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = state["msg"]
    group_list = await bot.get_group_list()
    succ_list = []
    err_list = []

    for group in group_list:
        await asyncio.sleep(randint(0, 2))
        try:
            await bot.send_group_msg(group_id=group["group_id"], message=msg)
        except BaseException:
            err_list.append(group["group_id"])

    msg0 = ""
    for i in err_list:
        msg0 += f"    {i}\n"

    repo_msg = (
        f"推送消息：\n{msg}\n"
        "————————\n"
        f"总共：{len(group_list)}\n"
        f"成功推送：{len(succ_list)}\n"
        f"失败[{len(err_list)}]个：\n"
    ) + msg0

    await broadcast.finish(repo_msg)
