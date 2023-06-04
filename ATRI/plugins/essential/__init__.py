import shutil
import asyncio
from pathlib import Path
from random import choice, randint

from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
    GroupIncreaseNoticeEvent,
    GroupDecreaseNoticeEvent,
    GroupAdminNoticeEvent,
    GroupBanNoticeEvent,
    GroupRecallNoticeEvent,
    FriendRecallNoticeEvent,
)

from ATRI import conf
from ATRI.log import log
from ATRI.service import Service
from ATRI.utils.apscheduler import scheduler
from ATRI.utils import MessageChecker
from ATRI.permission import MASTER
from ATRI.message import MessageBuilder

from .data_source import recall_msg_dealer


__ESSENTIAL_DIR = Path(".") / "data" / "plugins" / "essential"
__TEMP_DIR = Path(".") / "data" / "temp"
__ESSENTIAL_DIR.mkdir(parents=True, exist_ok=True)
__TEMP_DIR.mkdir(parents=True, exist_ok=True)

# __REJECT_RECALL_LIST = list()


plugin = Service("基础部件").document("对基础请求进行处理")


group_member_event = plugin.on_notice("群成员变动", "群成员变动检测")


@group_member_event.handle()
async def _(event: GroupIncreaseNoticeEvent):
    await asyncio.sleep(randint(1, 6))
    await group_member_event.finish(
        MessageBuilder("好欸! 事新人!").text(f"在下 {choice(list(conf.BotConfig.nickname))}")
    )


@group_member_event.handle()
async def _(event: GroupDecreaseNoticeEvent):
    await asyncio.sleep(randint(1, 6))
    await group_member_event.finish("呜——有人跑了...")


group_admin_event = plugin.on_notice("群管理变动", "群管理变动检测")


@group_admin_event.handle()
async def _(event: GroupAdminNoticeEvent):
    sub_type = event.sub_type
    if event.is_tome() and sub_type == "set":
        await plugin.send_to_master(f"好欸! 咱在群 {event.group_id} 成为了管理!!")
        return
    elif sub_type == "set":
        await group_admin_event.finish("新的py交易已达成")
    else:
        await group_admin_event.finish("有的人超能力到期了 (")


group_ban_event = plugin.on_notice("群禁言变动", "群禁言变动检测")


@group_ban_event.handle()
async def _(event: GroupBanNoticeEvent):
    if not event.is_tome():
        await group_ban_event.finish("群友喝下管理的红茶昏睡了过去")

    if event.duration:
        await plugin.send_to_master(
            MessageBuilder("那个...")
            .text(f"咱在群 {event.group_id} 被 {event.operator_id} 塞上了口球...")
            .text(f"时长...是 {event.duration} 秒")
        )
    else:
        await plugin.send_to_master(
            MessageBuilder("好欸!").text(
                f"咱在群 {event.group_id} 的口球被 {event.operator_id} 解除了!"
            )
        )


_acc_recall = True


recall_event = plugin.on_notice("撤回事件", "撤回事件检测")


@recall_event.handle()
async def _(bot: Bot, event: FriendRecallNoticeEvent):
    if not event.is_tome() and not _acc_recall:
        return

    try:
        repo = await bot.get_msg(message_id=event.message_id)
    except Exception:
        return

    log.debug(f"Recall raw msg:\n{repo}")
    user = event.user_id
    repo = repo["message"]

    try:
        m = recall_msg_dealer(repo)
    except Exception:
        check = MessageChecker(repo).check_cq_code
        if not check:
            m = repo
        else:
            return

    await plugin.send_to_master(
        MessageBuilder("咱拿到了一条撤回信息!").text(f"{user}@[私聊]").text(f"撤回了\n{m}")
    )


@recall_event.handle()
async def _(bot: Bot, event: GroupRecallNoticeEvent):
    if not event.is_tome() and not _acc_recall:
        return

    try:
        repo = await bot.get_msg(message_id=event.message_id)
    except Exception:
        return

    log.debug(f"Recall raw msg:\n{repo}")
    user = event.user_id
    group = event.group_id
    repo = repo["message"]

    try:
        m = recall_msg_dealer(repo)
    except Exception:
        check = MessageChecker(repo).check_cq_code
        if not check:
            m = repo
        else:
            return
    await plugin.send_to_master(
        MessageBuilder("咱拿到了一条撤回信息!").text(f"{user}@[群:{group}]").text(f"撤回了\n{m}")
    )


reject_recall = plugin.on_command("拒绝撤回", "拒绝撤回信息", permission=MASTER)


@reject_recall.handle()
async def _(event: MessageEvent):
    # global __REJECT_RECALL_LIST

    # user_id = event.get_user_id()
    # if not user_id in __REJECT_RECALL_LIST:
    #     __REJECT_RECALL_LIST.append(user_id)
    global _acc_recall

    _acc_recall = False
    await reject_recall.finish("完成~")


accept_recall = plugin.on_command("接受撤回", "接受撤回信息", permission=MASTER)


@accept_recall.handle()
async def _(event: MessageEvent):
    # global __REJECT_RECALL_LIST

    # user_id = event.get_user_id()
    # if user_id in __REJECT_RECALL_LIST:
    #     __REJECT_RECALL_LIST.remove(user_id)
    global _acc_recall

    _acc_recall = True
    await accept_recall.finish("完成~")


@scheduler.scheduled_job("interval", name="清除缓存", minutes=30, misfire_grace_time=5)  # type: ignore
async def _():
    try:
        shutil.rmtree(__TEMP_DIR)
        __TEMP_DIR.mkdir(parents=True, exist_ok=True)
    except Exception:
        log.warning("清除缓存失败, 请手动清除: data/temp")
