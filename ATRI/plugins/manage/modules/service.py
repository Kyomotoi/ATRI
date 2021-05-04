from nonebot.typing import T_State
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.adapters.cqhttp import (
    Bot,
    MessageEvent,
    GroupMessageEvent,
    PrivateMessageEvent,
)

from ATRI.service import Service as sv


__doc__ = """
启用功能，针对单群
权限组：维护者，群管理
用法：
  启用 目标命令
示例：
  启用 以图搜图 
"""

cur_service_ena = sv.on_command(
    cmd="启用功能", docs=__doc__, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER
)


@cur_service_ena.args_parser  # type: ignore
async def _cur_ena_load(bot: Bot, event: GroupMessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    quit_list = ["算了", "罢了", "取消"]
    if msg in quit_list:
        await cur_service_ena.finish("好吧...")
    if not msg:
        await cur_service_ena.reject("请告诉咱目标命令！")
    else:
        state["service_e"] = msg


@cur_service_ena.handle()
async def _cur_ena(bot: Bot, event: GroupMessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    if msg:
        state["service_e"] = msg


@cur_service_ena.got("service_e", prompt="请告诉咱目标命令！")
async def _deal_cur_ena(bot: Bot, event: GroupMessageEvent, state: T_State) -> None:
    cmd = state["service_e"]
    group = str(event.group_id)
    sv.control_service(cmd, False, True, group=group)
    await cur_service_ena.finish(f"成功！本群已启用：{cmd}")


@cur_service_ena.handle()
async def _refuse_cur_ena(bot: Bot, event: PrivateMessageEvent, state: T_State) -> None:
    await cur_service_ena.finish("只能在群聊中决定哦...")


__doc__ = """
禁用功能，针对单群
权限组：维护者，群管理
用法：
  禁用 目标命令
示例：
  禁用 以图搜图 
"""

cur_service_dis = sv.on_command(
    cmd="禁用功能", docs=__doc__, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER
)


@cur_service_dis.args_parser  # type: ignore
async def _cur_dis_load(bot: Bot, event: GroupMessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    quit_list = ["算了", "罢了", "取消"]
    if msg in quit_list:
        await cur_service_dis.finish("好吧...")
    if not msg:
        await cur_service_dis.reject("请告诉咱目标命令！")
    else:
        state["service_d"] = msg


@cur_service_dis.handle()
async def _cur_dis(bot: Bot, event: GroupMessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    if msg:
        state["service_d"] = msg


@cur_service_dis.got("service_d", prompt="请告诉咱目标命令！")
async def _deal_cur_dis(bot: Bot, event: GroupMessageEvent, state: T_State) -> None:
    cmd = state["service_d"]
    group = str(event.group_id)
    sv.control_service(cmd, False, False, group=group)
    await cur_service_dis.finish(f"成功！本群已禁用：{cmd}")


@cur_service_dis.handle()
async def _refuse_cur_dis(bot: Bot, event: PrivateMessageEvent, state: T_State) -> None:
    await cur_service_dis.finish("只能在群聊中决定哦...")


__doc__ = """
全局启用功能
权限组：维护者
用法：
  全局启用 目标命令
示例：
  全局启用 以图搜图
"""

glo_service_ena = sv.on_command(cmd="全局启用", docs=__doc__, permission=SUPERUSER)


@glo_service_ena.args_parser  # type: ignore
async def _glo_ena_load(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    quit_list = ["算了", "罢了", "取消"]
    if msg in quit_list:
        await glo_service_ena.finish("好吧...")
    if not msg:
        await glo_service_ena.reject("请告诉咱目标命令！")
    else:
        state["service_e_g"] = msg


@glo_service_ena.handle()
async def _glo_ena(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    if msg:
        state["service_e_g"] = msg


@glo_service_ena.got("service_e_g", prompt="请告诉咱目标命令！")
async def _deal_glo_ena(bot: Bot, event: MessageEvent, state: T_State) -> None:
    cmd = state["service_e_g"]
    sv.control_service(cmd, True, True)
    await glo_service_ena.finish(f"成功！已全局启用：{cmd}")


__doc__ = """
全局禁用功能
权限组：维护者
用法：
  全局禁用 目标命令
示例：
  全局禁用 以图搜图
"""

glo_service_dis = sv.on_command(cmd="全局禁用", docs=__doc__, permission=SUPERUSER)


@glo_service_dis.args_parser  # type: ignore
async def _glo_dis_load(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    quit_list = ["算了", "罢了", "取消"]
    if msg in quit_list:
        await glo_service_dis.finish("好吧...")
    if not msg:
        await glo_service_dis.reject("请告诉咱目标命令！")
    else:
        state["service_d_g"] = msg


@glo_service_dis.handle()
async def _glo_dis(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    if msg:
        state["service_d_g"] = msg


@glo_service_dis.got("service_d_g", prompt="请告诉咱目标命令！")
async def _deal_glo_dis(bot: Bot, event: MessageEvent, state: T_State) -> None:
    cmd = state["service_d_g"]
    sv.control_service(cmd, True, False)
    await glo_service_dis.finish(f"成功！已全局禁用：{cmd}")
