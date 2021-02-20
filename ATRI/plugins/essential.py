import time
import json
import shutil
from pathlib import Path
from random import choice

from nonebot.adapters import Bot
from nonebot.plugin import on_notice, on_request
from nonebot.adapters.cqhttp.message import Message
from nonebot.adapters.cqhttp import (
    FriendRequestEvent,
    GroupRequestEvent,
    GroupIncreaseNoticeEvent,
    GroupDecreaseNoticeEvent,
    GroupAdminNoticeEvent,
    GroupBanNoticeEvent,
    LuckyKingNotifyEvent,
    GroupUploadNoticeEvent,
    GroupRecallNoticeEvent,
    FriendRecallNoticeEvent
)

from ATRI.log import logger
from ATRI.exceptions import WriteError
from ATRI.config import nonebot_config
from ATRI.rule import is_in_banlist
from ATRI.service.httppost import HttpPost
from main import driver


PLUGIN_INFO_DIR = Path('.') / 'ATRI' / 'data' / 'service' / 'plugins'

@driver.on_startup
async def startup() -> None:
    logger.info("アトリは、高性能ですから！")


@driver.on_shutdown
async def shutdown() -> None:
    logger.info("Thanks for using.")
    logger.debug("bot已停止运行，正在清理插件信息...")
    try:
        shutil.rmtree(PLUGIN_INFO_DIR)
        logger.debug("成功！")
    except:
        repo = (
            '清理插件信息失败',
            '请前往 ATRI/data/service 下',
            '将 plugins 整个文件夹删除'
        )
        logger.error(repo)
        time.sleep(10)
        pass


@driver.on_bot_connect
async def connect(bot) -> None:
    for superuser in nonebot_config["superusers"]:
        await HttpPost.send_private_msg(
            int(superuser),
            "WebSocket 成功连接，数据开始传输。"
        )


@driver.on_bot_disconnect
async def disconnect(bot) -> None:
    for superuser in nonebot_config["superusers"]:
        try:
            await HttpPost.send_private_msg(
                int(superuser),
                "WebSocket 貌似断开了呢..."
            )
        except:
            logger.error("WebSocket 已断开，等待重连")


ESSENTIAL_DIR = Path('.') / 'ATRI' / 'data' / 'database' / 'essential'

# 处理：好友请求
request_friend_event = on_request(rule=is_in_banlist())

@request_friend_event.handle()
async def _request_friend_event(bot, event: FriendRequestEvent) -> None:
    file_name = "request_friend.json"
    path = ESSENTIAL_DIR / file_name
    path.parent.mkdir(exist_ok=True, parents=True)
    
    try:
        data = json.loads(path.read_bytes())
    except:
        data = {}
    data[event.flag] = {
        "user_id": event.user_id,
        "comment": event.comment
    }
    try:
        with open(path, 'w', encoding='utf-8') as r:
            r.write(
                json.dumps(
                    data, indent=4
                )
            )
    except WriteError:
        raise WriteError("Writing file failed!")
    
    for superuser in nonebot_config["superusers"]:
        msg = (
            "主人，收到一条好友请求：\n"
            f"请求人：{event.get_user_id()}\n"
            f"申请信息：{event.comment}\n"
            f"申请码：{event.flag}"
        )
        await HttpPost.send_private_msg(
            user_id=int(superuser),
            message=msg
        )


# 处理：邀请入群，如身为管理，还附有入群请求
request_group_event = on_request(rule=is_in_banlist())

@request_group_event.handle()
async def _request_group_event(bot, event: GroupRequestEvent) -> None:
    file_name = "request_group.json"
    path = ESSENTIAL_DIR / file_name
    path.parent.mkdir(exist_ok=True, parents=True)
    
    try:
        data = json.loads(path.read_bytes())
    except:
        data = {}
    data[event.flag] = {
        "user_id": event.user_id,
        "group_id": event.group_id,
        "sub_type": event.sub_type,
        "comment": event.comment
    }
    try:
        with open(path, 'w', encoding='utf-8') as r:
            r.write(
                json.dumps(
                    data, indent=4
                )
            )
    except WriteError:
        raise WriteError("Writing file failed!")
    
    for superuser in nonebot_config["superusers"]:
        msg = (
            "主人，收到一条入群请求：\n"
            f"请求人：{event.get_user_id()}\n"
            f"申请信息：{event.comment}\n"
            f"申请码：{event.flag}"
        )
        await HttpPost.send_private_msg(
            user_id=int(superuser),
            message=msg
        )
        

# 处理群成员变动
group_member_event = on_notice()

@group_member_event.handle()
async def _group_member_event(bot: Bot, event) -> None:
    if isinstance(event, GroupIncreaseNoticeEvent):
        msg = (
            "好欸！事新人！\n"
            f"在下 {choice(list(nonebot_config['nickname']))} 哒!w!"
        )
        await group_member_event.finish(msg)

    elif isinstance(event, GroupDecreaseNoticeEvent):
        if event.is_tome():
            msg = (
                "呜呜呜，主人"
                f"咱被群 {event.group_id} 里的 {event.operator_id} 扔出来了..."
            )
            for superuser in nonebot_config["superusers"]:
                await HttpPost.send_private_msg(
                    user_id=int(superuser),
                    message=msg
                )
        else:
            await group_member_event.finish(f"{event.user_id} 离开了我们...")


# 处理群管理事件
group_admin_event = on_notice()

@group_admin_event.handle()
async def _group_admin_event(bot: Bot, event: GroupAdminNoticeEvent) -> None:
    if event.is_tome():
        for superuser in nonebot_config["superusers"]:
            await HttpPost.send_private_msg(
                user_id=int(superuser),
                message=f"好欸！主人！我在群 {event.group_id} 成为了管理！！"
            )


# 处理群禁言事件
group_ban_event = on_notice()

@group_ban_event.handle()
async def _group_ban_event(bot: Bot, event: GroupBanNoticeEvent) -> None:
    if event.is_tome():
        if event.duration:
            msg = (
                "那个..。，主人\n"
                f"咱在群 {event.group_id} 被 {event.operator_id} 塞上了口球...\n"
                f"时长...是 {event.duration} 秒"
            )
            for superuser in nonebot_config["superusers"]:
                await HttpPost.send_private_msg(
                    user_id=int(superuser),
                    message=msg
                )
        else:
            msg = (
                "好欸！主人\n"
                f"咱在群 {event.group_id} 被 {event.operator_id} 上的口球解除了！"
            )
            for superuser in nonebot_config["superusers"]:
                await HttpPost.send_private_msg(
                    user_id=int(superuser),
                    message=msg
                )


# 处理群红包运气王事件
lucky_read_bag_event = on_notice()

@lucky_read_bag_event.handle()
async def _lucky_read_bag_event(bot, event: LuckyKingNotifyEvent) -> None:
    msg = (
        "8行，这可忍？"
        f"gkd [CQ:at,qq={event.user_id}] 发一个！"
    )
    await lucky_read_bag_event.finish(Message(msg))


# 处理群文件上传事件
group_file_upload_event = on_notice()

@group_file_upload_event.handle()
async def _group_file_upload_event(bot,
                                   event: GroupUploadNoticeEvent) -> None:
    await group_file_upload_event.finish("让我康康传了啥好东西")


# 处理撤回事件
recall_event = on_notice()

@recall_event.handle()
async def _recall_event(bot: Bot, event) -> None:
    if isinstance(event, GroupRecallNoticeEvent):
        repo = await bot.call_api(
            "get_msg",
            message_id=event.message_id
        )
        repo = str(repo["message"])
        if "CQ" in repo:
            repo = repo.replace("CQ", "QC")

        msg = (
            "主人，咱拿到了一条撤回信息！\n"
            f"{event.user_id}@[群:{event.group_id}]\n"
            "撤回了\n"
            f"{repo}"
        )

        await bot.send(event, "咱看到惹~！")
        for superuser in nonebot_config["superusers"]:
            await HttpPost.send_private_msg(
                user_id=int(superuser),
                message=msg
            )

    elif isinstance(event, FriendRecallNoticeEvent):
        repo = await bot.call_api(
            "get_msg",
            message_id=event.message_id
        )
        repo = str(repo["message"])
        if "CQ" in repo:
            repo = repo.replace("CQ", "QC")

        msg = (
            "主人，咱拿到了一条撤回信息！\n"
            f"{event.user_id}@[私聊]"
            "撤回了\n"
            f"{repo}"
        )

        for superuser in nonebot_config["superusers"]:
            await HttpPost.send_private_msg(
                user_id=int(superuser),
                message=msg
            )
