import re
from datetime import datetime
from typing import Type, Callable
from asyncio import iscoroutinefunction

from nonebot.matcher import Matcher
from nonebot.params import ArgPlainText, CommandArg
from nonebot.adapters.onebot.v11 import (
    Bot,
    Message,
    MessageEvent,
    FriendRequestEvent,
    GroupRequestEvent,
)

from ATRI.rule import to_bot
from ATRI.service import Service
from ATRI.message import MessageBuilder
from ATRI.permission import MASTER, ADMIN

from .models import RequestInfo
from .data_source import BotManager
from .plugin import NonebotPluginManager


_QUIT_ARGS = ["算了", "罢了"]


def handle_command(
    plugin: Type[Matcher],
    func: Callable,
    success_msg: str,
    fail_msg: str = "操作 {} 失败...原因：\n{}",
):
    @plugin.handle()
    async def handle_command(matcher: Matcher, args: Message = CommandArg()):
        msg = args.extract_plain_text()
        if msg:
            matcher.set_arg("target", args)

    @plugin.got("target", "要操作的目标是？")
    async def handle_target(event: MessageEvent, target: str = ArgPlainText("target")):
        if target in _QUIT_ARGS:
            await plugin.finish("好吧")

        try:
            func_argcount = func.__code__.co_argcount
            if iscoroutinefunction(func):
                if func_argcount == 3:
                    result = await func(target, event)
                else:
                    result = await func(target)
            else:
                if func_argcount == 3:
                    result = func(target, event)
                else:
                    result = func(target)
            msg = success_msg.format(target)
            if type(result) == bool:
                msg += "启用" if result else "禁用"
            await plugin.send(msg.format(target))
        except Exception as e:
            error_msg = str(e)
            await plugin.send(fail_msg.format(target, error_msg))


plugin = Service("管理").document("控制 ATRI 的各项服务").only_admin(True).permission(MASTER)


block_user = plugin.on_command("封禁用户", "阻止目标用户使用 ATRI")
handle_command(block_user, BotManager().block_user, "用户 {} 危！")


unblock_user = plugin.on_command("解封用户", "对被阻止的用户解封")
handle_command(unblock_user, BotManager().unblock_user, "用户 {} 已解封")


block_group = plugin.on_command("封禁群", "阻止目标群所有人使用 ATRI")
handle_command(block_group, BotManager().block_group, "群 {} 危！")


unblock_group = plugin.on_command("解封群", "对被阻止的群解封")
handle_command(unblock_group, BotManager().unblock_group, "群 {} 已解封")


toggle_global_service = plugin.on_command("全局控制", "全局禁用/启用某一服务")
handle_command(
    toggle_global_service,
    BotManager().toggle_global_service,
    "服务 {} 已全局",
)


toggle_group_service = plugin.on_command("控制", "针对所在群禁用/启用某一服务", permission=ADMIN)
handle_command(
    toggle_group_service,
    BotManager().toggle_group_service,
    "服务 {} 已针对本群",
)


track_error = plugin.on_command("追踪", "根据ID获取对应报错信息", aliases={"/track"})
handle_command(
    track_error,
    BotManager().track_error,
    "{}",
)


apply_friend_req = plugin.on_command("同意好友", "根据申请码同意对应好友申请")
handle_command(apply_friend_req, BotManager().apply_friend_req, "已同意该申请")


reject_friend_req = plugin.on_command("拒绝好友", "根据申请码拒绝对应好友申请")
handle_command(reject_friend_req, BotManager().reject_friend_req, "已拒绝该申请")


apply_group_req = plugin.on_command("同意邀请", "根据申请码同意对应群邀请")
handle_command(apply_group_req, BotManager().apply_group_req, "已同意该邀请")


reject_group_req = plugin.on_command("拒绝邀请", "根据申请码拒绝对应群邀请")
handle_command(reject_group_req, BotManager().reject_group_req, "已拒绝该邀请")


toggle_user_service = plugin.on_regex(r"对用户(.*?)(启用|禁用)(.*)", "针对单一用户禁用/启用某一服务")


@toggle_user_service.handle()
async def _(event: MessageEvent):
    msg = str(event.get_message()).strip()
    reg = re.findall("对用户(.*?)(启用|禁用)(.*)", msg)[0]
    target_user = reg[0]
    target_service = reg[2]

    try:
        result = BotManager().toggle_user_service(target_service, target_user)
    except Exception as e:
        await toggle_user_service.finish(f"操作失败，原因：{str(e)}")
    await toggle_user_service.finish(
        f"已{'允许' if result else '禁止'}用户 {target_user} 使用 {target_service}"
    )


friend_req = plugin.on_request("好友申请", "好友申请检测")


@friend_req.handle()
async def _(event: FriendRequestEvent):
    apply_code = event.flag
    user_id = event.get_user_id()
    apply_comment = event.comment
    now_time = str(datetime.now().timestamp())

    data = await BotManager().load_friend_req()
    data[apply_code] = RequestInfo(
        user_id=user_id,
        comment=apply_comment,
        time=now_time,
    )
    await BotManager().store_friend_req(data)

    result = (
        MessageBuilder("咱收到一条好友请求！")
        .text(f"请求人：{user_id}")
        .text(f"申请信息：{apply_comment}")
        .text(f"申请码：{apply_code}")
        .text("Tip：好友申请列表")
    )
    await plugin.send_to_master(result)


group_req = plugin.on_request("应邀入群", "应邀入群检测")


@group_req.handle()
async def _(event: GroupRequestEvent):
    if event.sub_type != "invite":
        return

    apply_code = event.flag
    target_group = event.group_id
    user_id = event.get_user_id()
    apply_comment = event.comment
    now_time = str(datetime.now().timestamp())

    data = await BotManager().load_group_req()
    data[apply_code] = RequestInfo(
        user_id=user_id,
        comment=apply_comment + f"(目标群{target_group})",
        time=now_time,
    )
    await BotManager().store_group_req(data)

    result = (
        MessageBuilder("咱收到一条应邀入群请求！")
        .text(f"申请人：{user_id}")
        .text(f"申请信息：{apply_comment}")
        .text(f"申请码：{apply_code}")
        .text(f"目标群：{target_group}")
        .text("Tip：群邀请列表")
    )
    await plugin.send_to_master(result)


get_friend_req_list = plugin.on_command("好友申请列表", "获取好友申请列表")


@get_friend_req_list.handle()
async def _():
    data = await BotManager().load_friend_req()
    if not data:
        await get_friend_req_list.finish("当前没有申请")

    cache_list = list()
    for i in data:
        apply_code = i
        apply_user = data[i].user_id
        apply_comment = data[i].comment
        cache_list.append(f"{apply_user} | {apply_comment} | {apply_code}")

    result = (
        "申请人ID | 申请信息 | 申请码\n"
        + "\n".join(map(str, cache_list))
        + "\nTip: 使用 同意/拒绝好友 [申请码] 以决定"
    )
    await get_friend_req_list.finish(result)


get_group_req_list = plugin.on_command("群邀请列表", "获取群邀请列表")


@get_group_req_list.handle()
async def _():
    data = await BotManager().load_group_req()
    if not data:
        await get_group_req_list.finish("当前没有申请")

    cache_list = list()
    for i in data:
        apply_code = i
        apply_user = data[i].user_id
        apply_comment = data[i].comment
        cache_list.append(f"{apply_user} | {apply_comment} | {apply_code}")

    result = (
        "申请人ID | 申请信息 | 申请码\n"
        + "\n".join(map(str, cache_list))
        + "\nTip: 使用 同意/拒绝邀请 [申请码] 以决定"
    )
    await get_group_req_list.finish(result)


recall_msg = plugin.on_command("撤回", "撤回 ATRI 已发送的信息", to_bot())


@recall_msg.handle()
async def _recall_msg(bot: Bot, event: MessageEvent):
    try:
        recall_id = event.reply.message_id  # type: ignore
    except Exception:
        await recall_msg.finish("无法获取必要信息...没法撤回惹...")

    await bot.delete_msg(message_id=recall_id)


add_nonebot_plugin = plugin.on_command("添加插件", "添加来自 NoneBot 商店的插件")


@add_nonebot_plugin.got("plugin_name", "插件名呢?")
async def _(plugin_name: str = ArgPlainText("plugin_name")):
    nbm = NonebotPluginManager().assign_plugin(plugin_name)

    if nbm.plugin_is_exist(True):
        await add_nonebot_plugin.finish("该插件已存在")

    if not (plugin_info := nbm.get_plugin_info()):
        await add_nonebot_plugin.finish("未找到该插件")

    msg = (
        MessageBuilder(f"[{plugin_name}]")
        .text(f"名称: {plugin_info.name}")
        .text(f"说明: {plugin_info.desc}")
        .text(f"作者: {plugin_info.author}")
        .text(f"插件主页: {plugin_info.homepage}")
        .text(f"{str() if plugin_info.is_official else '[!] 非'}官方插件")
    )
    await add_nonebot_plugin.send(msg)


@add_nonebot_plugin.got("att", "是否安装(y/n)")
async def _(
    att: str = ArgPlainText("att"), plugin_name: str = ArgPlainText("plugin_name")
):
    if att not in ["y", "Y", "是"]:
        await add_nonebot_plugin.finish("反悔了呢")

    nbm = NonebotPluginManager().assign_plugin(plugin_name)
    result = nbm.add_plugin()
    await add_nonebot_plugin.finish(result)


remove_nonebot_plugin = plugin.on_command(
    "移除插件", "移除来自 NoneBot 商店的插件", aliases={"删除插件", "卸载插件"}
)


@remove_nonebot_plugin.got("plugin_name", "要移除的插件名呢?")
@remove_nonebot_plugin.got("att", "确定吗(y/n)")
async def _(
    att: str = ArgPlainText("att"), plugin_name: str = ArgPlainText("plugin_name")
):
    if att not in ["y", "Y", "是"]:
        await remove_nonebot_plugin.finish("反悔了呢")

    nbm = NonebotPluginManager().assign_plugin(plugin_name)
    result = nbm.remove_plugin()
    await remove_nonebot_plugin.finish(result)


upgrade_nonebot_plugin = plugin.on_command(
    "更新插件", "更新来自 NoneBot 商店的插件", aliases={"升级插件"}
)


@upgrade_nonebot_plugin.handle()
async def _(event: MessageEvent):
    result = NonebotPluginManager().upgrade_plugin()
    if not result:
        await upgrade_nonebot_plugin.finish("当前没有插件可更新...")

    msg = "更新完成~! 成功更新:" + "\n".join(map(str, result))
    await upgrade_nonebot_plugin.finish(msg)


from ATRI import driver
from ATRI.utils.apscheduler import scheduler

from .listener import init_listener

driver().on_startup(init_listener)
driver().on_startup(NonebotPluginManager().get_store_list)
driver().on_startup(NonebotPluginManager().load_plugin)
scheduler.scheduled_job(
    "interval",
    name="NoneBot 商店刷新",
    hours=1,
    max_instances=3,
    misfire_grace_time=60,
)(NonebotPluginManager().get_store_list)
