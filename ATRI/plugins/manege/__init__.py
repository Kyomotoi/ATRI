import re

from nonebot.typing import T_State
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent
from nonebot.adapters.cqhttp.permission import GROUP_OWNER, GROUP_ADMIN

from .data_source import Manege


# 求1个pr把这里优化，写得我想吐了


block_user = Manege().on_command("封禁用户", "对目标用户进行封禁", permission=SUPERUSER)

@block_user.args_parser  # type: ignore
async def _get_block_user(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    quit_list = ["算了", "罢了"]
    if msg in quit_list:
        await block_user.finish("...看来有人逃过一劫呢")
    if not msg:
        await block_user.reject("哪位？GKD！")
    else:
        state["block_user"] = msg

@block_user.handle()
async def _ready_block_user(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    if msg:
        state["block_user"] = msg

@block_user.got("block_user", "哪位？GKD！")
async def _deal_block_user(bot: Bot, event: MessageEvent, state: T_State):
    user_id = state["block_user"]
    is_ok = Manege().block_user(user_id)
    if not is_ok:
        await block_user.finish("kuso！封禁失败了...")
    
    await block_user.finish(f"用户 {user_id} 危！")


unblock_user = Manege().on_command("解封用户", "对目标用户进行解封", permission=SUPERUSER)

@unblock_user.args_parser  # type: ignore
async def _get_unblock_user(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    quit_list = ["算了", "罢了"]
    if msg in quit_list:
        await unblock_user.finish("...有人又得继续在小黑屋呆一阵子了")
    if not msg:
        await unblock_user.reject("哪位？GKD！")
    else:
        state["unblock_user"] = msg

@unblock_user.handle()
async def _ready_unblock_user(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    if msg:
        state["unblock_user"] = msg

@unblock_user.got("unblock_user", "哪位？GKD！")
async def _deal_unblock_user(bot: Bot, event: MessageEvent, state: T_State):
    user_id = state["unblock_user"]
    is_ok = Manege().unblock_user(user_id)
    if not is_ok:
        await unblock_user.finish("kuso！解封失败了...")
    
    await unblock_user.finish(f"好欸！{user_id} 重获新生！")


block_group = Manege().on_command("封禁群", "对目标群进行封禁", permission=SUPERUSER)

@block_group.args_parser  # type: ignore
async def _get_block_group(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    quit_list = ["算了", "罢了"]
    if msg in quit_list:
        await block_group.finish("...看来有一群逃过一劫呢")
    if not msg:
        await block_group.reject("哪个群？GKD！")
    else:
        state["block_group"] = msg

@block_group.handle()
async def _ready_block_group(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    if msg:
        state["block_group"] = msg

@block_group.got("block_group", "哪个群？GKD！")
async def _deal_block_group(bot: Bot, event: MessageEvent, state: T_State):
    group_id = state["block_group"]
    is_ok = Manege().block_group(group_id)
    if not is_ok:
        await block_group.finish("kuso！封禁失败了...")
    
    await block_group.finish(f"群 {group_id} 危！")


unblock_group = Manege().on_command("解封群", "对目标群进行解封", permission=SUPERUSER)

@unblock_group.args_parser  # type: ignore
async def _get_unblock_group(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    quit_list = ["算了", "罢了"]
    if msg in quit_list:
        await unblock_group.finish("...有一群又得继续在小黑屋呆一阵子了")
    if not msg:
        await unblock_group.reject("哪个群？GKD！")
    else:
        state["unblock_group"] = msg

@unblock_group.handle()
async def _ready_unblock_group(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    if msg:
        state["unblock_group"] = msg

@unblock_group.got("unblock_group", "哪个群？GKD！")
async def _deal_unblock_group(bot: Bot, event: MessageEvent, state: T_State):
    group_id = state["unblock_group"]
    is_ok = Manege().unblock_group(group_id)
    if not is_ok:
        await unblock_group.finish("kuso！解封失败了...")
    
    await unblock_group.finish(f"好欸！群 {group_id} 重获新生！")


global_block_service = Manege().on_command("全局禁用", "全局禁用某服务", permission=SUPERUSER)

@global_block_service.args_parser  # type: ignore
async def _get_global_block_service(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    quit_list = ["算了", "罢了"]
    if msg in quit_list:
        await global_block_service.finish("好吧...")
    if not msg:
        await global_block_service.reject("阿...是哪个服务呢")
    else:
        state["global_block_service"] = msg

@global_block_service.handle()
async def _ready_block_service(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    if msg:
        state["global_block_service"] = msg

@global_block_service.got("global_block_service", "阿...是哪个服务呢")
async def _deal_global_block_service(bot: Bot, event: MessageEvent, state: T_State):
    block_service = state["global_block_service"]
    is_ok = Manege().control_global_service(block_service, False)
    if not is_ok:
        await global_block_service.finish("kuso！禁用失败了...")
    
    await global_block_service.finish(f"服务 {block_service} 已被禁用")


global_unblock_service = Manege().on_command("全局启用", "全局启用某服务", permission=SUPERUSER)

@global_unblock_service.args_parser  # type: ignore
async def _get_global_unblock_service(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    quit_list = ["算了", "罢了"]
    if msg in quit_list:
        await global_unblock_service.finish("好吧...")
    if not msg:
        await global_unblock_service.reject("阿...是哪个服务呢")
    else:
        state["global_unblock_service"] = msg

@global_unblock_service.handle()
async def _ready_unblock_service(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    if msg:
        state["global_unblock_service"] = msg

@global_unblock_service.got("global_unblock_service", "阿...是哪个服务呢")
async def _deal_global_unblock_service(bot: Bot, event: MessageEvent, state: T_State):
    block_service = state["global_unblock_service"]
    is_ok = Manege().control_global_service(block_service, True)
    if not is_ok:
        await global_unblock_service.finish("kuso！启用服务失败了...")
    
    await global_unblock_service.finish(f"服务 {block_service} 已启用")


user_block_service = Manege().on_regex(r"对用户(.*?)禁用(.*)", "针对某一用户禁用服务", permission=SUPERUSER)

@user_block_service.handle()
async def _user_block_service(bot: Bot, event: MessageEvent):
    msg = str(event.message).strip()
    pattern = r"对用户(.*?)禁用(.*)"
    reg = re.findall(pattern, msg)
    aim_user = reg[0]
    aim_service = reg[1]
    
    is_ok = Manege().control_user_service(aim_service, aim_user, False)
    if not is_ok:
        await user_block_service.finish("禁用失败...请检查服务名是否正确")
    await user_block_service.finish(f"完成～已禁止用户 {aim_user} 使用 {aim_service}")
    


user_unblock_service = Manege().on_regex(r"对用户(.*?)启用(.*)", "针对某一用户启用服务", permission=SUPERUSER)

@user_unblock_service.handle()
async def _user_unblock_service(bot: Bot, event: MessageEvent):
    msg = str(event.message).strip()
    pattern = r"对用户(.*?)启用(.*)"
    reg = re.findall(pattern, msg)
    aim_user = reg[0]
    aim_service = reg[1]
    
    is_ok = Manege().control_user_service(aim_service, aim_user, True)
    if not is_ok:
        await user_unblock_service.finish("启用失败...请检查服务名是否正确，或者此人并不存在于名单中")
    await user_unblock_service.finish(f"完成～已允许用户 {aim_user} 使用 {aim_service}")


group_block_service = Manege().on_command("禁用", "针对所在群禁用某服务", permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN)

@group_block_service.args_parser  # type: ignore
async def _get_group_block_service(bot: Bot, event: GroupMessageEvent, state: T_State):
    msg = str(event.message).strip()
    quit_list = ["算了", "罢了"]
    if msg in quit_list:
        await group_block_service.finish("好吧...")
    if not msg:
        await group_block_service.reject("阿...是哪个服务呢")
    else:
        state["group_block_service"] = msg

@group_block_service.handle()
async def _ready_group_block_service(bot: Bot, event: GroupMessageEvent, state: T_State):
    msg = str(event.message).strip()
    if msg:
        state["group_block_service"] = msg

@group_block_service.got("group_block_service", "阿...是哪个服务呢")
async def _deal_group_block_service(bot: Bot, event: GroupMessageEvent, state: T_State):
    aim_service = state["group_block_service"]
    group_id = str(event.group_id)
    
    is_ok = Manege().control_group_service(aim_service, group_id, False)
    if not is_ok:
        await group_block_service.finish("禁用失败...请检查服务名是否输入正确")
    await group_block_service.finish(f"完成！～已禁止本群使用服务：{aim_service}")


group_unblock_service = Manege().on_command("启用", "针对所在群启用某服务", permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN)

@group_unblock_service.args_parser  # type: ignore
async def _get_group_unblock_service(bot: Bot, event: GroupMessageEvent, state: T_State):
    msg = str(event.message).strip()
    quit_list = ["算了", "罢了"]
    if msg in quit_list:
        await group_unblock_service.finish("好吧...")
    if not msg:
        await group_unblock_service.reject("阿...是哪个服务呢")
    else:
        state["group_unblock_service"] = msg

@group_unblock_service.handle()
async def _ready_group_unblock_service(bot: Bot, event: GroupMessageEvent, state: T_State):
    msg = str(event.message).strip()
    if msg:
        state["group_unblock_service"] = msg

@group_unblock_service.got("group_unblock_service", "阿...是哪个服务呢")
async def _deal_group_unblock_service(bot: Bot, event: GroupMessageEvent, state: T_State):
    aim_service = state["group_unblock_service"]
    group_id = str(event.group_id)
    
    is_ok = Manege().control_group_service(aim_service, group_id, True)
    if not is_ok:
        await group_unblock_service.finish("启用失败...请检查服务名是否输入正确，或群不存在于名单中")
    await group_unblock_service.finish(f"完成！～已允许本群使用服务：{aim_service}")


get_friend_add_list = Manege().on_command("获取好友申请", "获取好友申请列表", permission=SUPERUSER)

@get_friend_add_list.handle()
async def _get_friend_add_list(bot: Bot, event: MessageEvent):
    data = Manege().load_friend_apply_list()
    temp_list = list()
    for i in data:
        apply_code = i
        apply_user = data[i]["user_id"]
        apply_comment = data[i]["comment"]
        temp_msg = f"{apply_user} | {apply_comment} | {apply_code}"
        temp_list.append(temp_msg)

    msg0 = "申请人ID | 申请信息 | 申请码\n" + "\n".join(map(str, temp_list))
    msg1 = msg0 + "\nTip: 使用 同意/拒绝好友 [申请码] 以决定"
    await get_friend_add_list.finish(msg1)
    

approve_friend_add = Manege().on_command("同意好友", "同意好友申请", permission=SUPERUSER)

@approve_friend_add.args_parser  # type: ignore
async def _get_approve_friend_add(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    quit_list = ["算了", "罢了"]
    if msg in quit_list:
        await approve_friend_add.finish("好吧...")
    if not msg:
        await approve_friend_add.reject("申请码GKD！")
    else:
        state["approve_friend_add"] = msg

@approve_friend_add.handle()
async def _ready_approve_friend_add(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    if msg:
        state["approve_friend_add"]

@approve_friend_add.got("approve_friend_add", "申请码GKD!")
async def _deal_approve_friend_add(bot: Bot, event: MessageEvent, state: T_State):
    apply_code = state["approve_friend_add"]
    try:
        await bot.set_friend_add_request(flag=apply_code, approve=True)
    except BaseException:
        await approve_friend_add.finish("同意失败...尝试下手动？")
    data = Manege().load_friend_apply_list()
    data.pop(apply_code)
    Manege().save_friend_apply_list(data)
    await approve_friend_add.finish("好欸！申请已通过！")


refuse_friend_add = Manege().on_command("拒绝好友", "拒绝好友申请", permission=SUPERUSER)

@refuse_friend_add.args_parser  # type: ignore
async def _get_refuse_friend_add(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    quit_list = ["算了", "罢了"]
    if msg in quit_list:
        await refuse_friend_add.finish("好吧...")
    if not msg:
        await refuse_friend_add.reject("申请码GKD！")
    else:
        state["refuse_friend_add"] = msg

@refuse_friend_add.handle()
async def _ready_refuse_friend_add(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    if msg:
        state["refuse_friend_add"]

@refuse_friend_add.got("refuse_friend_add", "申请码GKD!")
async def _deal_refuse_friend_add(bot: Bot, event: MessageEvent, state: T_State):
    apply_code = state["refuse_friend_add"]
    try:
        await bot.set_friend_add_request(flag=apply_code, approve=False)
    except BaseException:
        await refuse_friend_add.finish("拒绝失败...尝试下手动？")
    data = Manege().load_friend_apply_list()
    data.pop(apply_code)
    Manege().save_friend_apply_list(data)
    await refuse_friend_add.finish("已拒绝！")


get_group_invite_list = Manege().on_command("获取邀请列表", "获取群邀请列表", permission=SUPERUSER)

@get_group_invite_list.handle()
async def _get_group_invite_list(bot: Bot, event: MessageEvent):
    data = Manege().load_invite_apply_list()
    temp_list = list()
    for i in data:
        apply_code = i
        apply_user = data[i]["user_id"]
        apply_comment = data[i]["comment"]
        temp_msg = f"{apply_user} | {apply_comment} | {apply_code}"
        temp_list.append(temp_msg)

    msg0 = "申请人ID | 申请信息 | 申请码\n" + "\n".join(map(str, temp_list))
    msg1 = msg0 + "\nTip: 使用 同意/拒绝邀请 [申请码] 以决定"
    await get_friend_add_list.finish(msg1)


approve_group_invite = Manege().on_command("同意邀请", "同意群聊邀请", permission=SUPERUSER)

@approve_group_invite.args_parser  # type: ignore
async def _get_approve_group_invite(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    quit_list = ["算了", "罢了"]
    if msg in quit_list:
        await approve_group_invite.finish("好吧...")
    if not msg:
        await approve_group_invite.reject("申请码GKD！")
    else:
        state["approve_group_invite"] = msg

@approve_group_invite.handle()
async def _ready_approve_group_invite(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    if msg:
        state["approve_group_invite"]

@approve_group_invite.got("approve_group_invite", "申请码GKD!")
async def _deal_approve_group_invite(bot: Bot, event: MessageEvent, state: T_State):
    apply_code = state["approve_group_invite"]
    try:
        await bot.set_group_add_request(flag=apply_code, sub_type="invite", approve=True)
    except BaseException:
        await approve_group_invite.finish("同意失败...尝试下手动？")
    data = Manege().load_invite_apply_list()
    data.pop(apply_code)
    Manege().save_invite_apply_list(data)
    await approve_group_invite.finish("好欸！申请已通过！")


refuse_group_invite = Manege().on_command("拒绝邀请", "拒绝群聊邀请", permission=SUPERUSER)

@refuse_group_invite.args_parser  # type: ignore
async def _get_refuse_group_invite(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    quit_list = ["算了", "罢了"]
    if msg in quit_list:
        await refuse_group_invite.finish("好吧...")
    if not msg:
        await refuse_group_invite.reject("申请码GKD！")
    else:
        state["refuse_group_invite"] = msg

@refuse_group_invite.handle()
async def _ready_refuse_group_invite(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    if msg:
        state["refuse_group_invite"]

@refuse_group_invite.got("refuse_group_invite", "申请码GKD!")
async def _deal_refuse_group_invite(bot: Bot, event: MessageEvent, state: T_State):
    apply_code = state["refuse_group_invite"]
    try:
        await bot.set_group_add_request(flag=apply_code, sub_type="invite", approve=False)
    except BaseException:
        await refuse_group_invite.finish("拒绝失败...尝试下手动？")
    data = Manege().load_invite_apply_list()
    data.pop(apply_code)
    Manege().save_invite_apply_list(data)
    await refuse_group_invite.finish("已拒绝！")


track_error = Manege().on_command("追踪", "获取报错信息，传入追踪码", aliases={"/track"})

@track_error.handle()
async def _track_error(bot: Bot, event: MessageEvent):
    track_id = str(event.message).strip()
    repo = await Manege().track_error(track_id)
    await track_error.finish(repo)
