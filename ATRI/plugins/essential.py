import os
import time
import json
import shutil
from pathlib import Path
from random import choice
from datetime import datetime

from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.message import run_preprocessor
from nonebot.exception import IgnoredException
from nonebot.adapters.cqhttp.message import Message
from nonebot.adapters.cqhttp import (
    Bot,
    MessageEvent,
    GroupMessageEvent,
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

import ATRI
from ATRI.log import logger
from ATRI.exceptions import WriteError
from ATRI.config import Config
from ATRI.service import Service as sv
from ATRI.utils.cqcode import coolq_code_check


PLUGIN_INFO_DIR = Path('.') / 'ATRI' / 'data' / 'service' / 'services'
ESSENTIAL_DIR = Path('.') / 'ATRI' / 'data' / 'database' / 'essential'
os.makedirs(PLUGIN_INFO_DIR, exist_ok=True)
os.makedirs(ESSENTIAL_DIR, exist_ok=True)


driver = ATRI.driver()


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
    except Exception:
        repo = (
            '清理插件信息失败',
            '请前往 ATRI/data/service/services 下',
            '将 services 整个文件夹删除'
        )
        time.sleep(10)
        raise Exception(repo)


@driver.on_bot_connect
async def connect(bot) -> None:
    for superuser in Config.BotSelfConfig.superusers:
        await sv.NetworkPost.send_private_msg(
            int(superuser),
            "WebSocket 成功连接，数据开始传输。"
        )


@driver.on_bot_disconnect
async def disconnect(bot) -> None:
    for superuser in Config.BotSelfConfig.superusers:
        try:
            await sv.NetworkPost.send_private_msg(
                int(superuser),
                "WebSocket 貌似断开了呢..."
            )
        except:
            logger.error("WebSocket 已断开，等待重连")


@run_preprocessor  # type: ignore
async def _check_block(matcher: Matcher,
                       bot: Bot,
                       event: MessageEvent,
                       state: T_State) -> None:
    user = str(event.user_id)
    msg = str(event.message)
    if not sv.BlockSystem.auth_user(user):
        raise IgnoredException(f'Block user: {user}')
    
    if not sv.Dormant.is_dormant():
        if "/dormant" not in msg:
            raise IgnoredException('Bot has been dormant.')
    
    if isinstance(event, GroupMessageEvent):
        group = str(event.group_id)
        if not sv.BlockSystem.auth_group(group):
            raise IgnoredException(f'Block group: {group}')


@run_preprocessor  # type: ignore
async def _store_message(matcher: Matcher,
                         bot: Bot,
                         event,
                         state: T_State) -> None:
    if isinstance(event, GroupMessageEvent):
        if event.sub_type == "normal":
            now_time = datetime.now().strftime('%Y-%m-%d') 
            GROUP_DIR = ESSENTIAL_DIR / 'chat_history' / f'{event.group_id}'
            os.makedirs(GROUP_DIR, exist_ok=True)
            path = GROUP_DIR / f"{now_time}.chat.json"
            now_time = datetime.now().strftime('%Y%m%d-%H%M%S')

            try:
                data = json.loads(path.read_bytes())
            except:
                data = dict()
            data[str(event.message_id)] = {
                "date": now_time,
                "time": str(time.time()),
                "post_type": str(event.post_type),
                "sub_type": str(event.sub_type),
                "user_id": str(event.user_id),
                "group_id": str(event.group_id),
                "message_type": str(event.message_type),
                "message": str(event.message),
                "raw_message": event.raw_message,
                "font": str(event.font),
                "sender": {
                    "user_id": str(event.sender.user_id),
                    "nickname": event.sender.nickname,
                    "sex": event.sender.sex,
                    "age": str(event.sender.age),
                    "card": event.sender.card,
                    "area": event.sender.area,
                    "level": event.sender.level,
                    "role": event.sender.role,
                    "title": event.sender.title
                },
                "to_me": str(event.to_me)
            }
            try:
                with open(path, 'w', encoding='utf-8') as r:
                    r.write(json.dumps(data, indent=4))
                logger.debug(f"写入消息成功，id: {event.message_id}")
            except WriteError:
                logger.error("消息记录失败，可能是缺少文件的原因！")
            else:
                pass
        else:
            pass
    else:
        pass


# 处理：好友请求
request_friend_event = sv.on_request()

@request_friend_event.handle()
async def _request_friend_event(bot, event: FriendRequestEvent) -> None:
    file_name = "request_friend.json"
    path = ESSENTIAL_DIR / file_name
    path.parent.mkdir(exist_ok=True, parents=True)
    
    try:
        data = json.loads(path.read_bytes())
    except:
        data = dict()
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
    
    for superuser in Config.BotSelfConfig.superusers:
        msg = (
            "主人，收到一条好友请求：\n"
            f"请求人：{event.get_user_id()}\n"
            f"申请信息：{event.comment}\n"
            f"申请码：{event.flag}"
        )
        await sv.NetworkPost.send_private_msg(
            user_id=int(superuser),
            message=msg
        )


# 处理：邀请入群，如身为管理，还附有入群请求
request_group_event = sv.on_request()

@request_group_event.handle()
async def _request_group_event(bot, event: GroupRequestEvent) -> None:
    file_name = "request_group.json"
    path = ESSENTIAL_DIR / file_name
    path.parent.mkdir(exist_ok=True, parents=True)
    
    try:
        data = json.loads(path.read_bytes())
    except:
        data = dict()
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
    
    for superuser in Config.BotSelfConfig.superusers:
        msg = (
            "主人，收到一条入群请求：\n"
            f"请求人：{event.get_user_id()}\n"
            f"申请信息：{event.comment}\n"
            f"申请码：{event.flag}"
        )
        await sv.NetworkPost.send_private_msg(
            user_id=int(superuser),
            message=msg
        )
        

# 处理群成员变动
group_member_event = sv.on_notice()

@group_member_event.handle()
async def _group_member_event(bot: Bot, event: GroupIncreaseNoticeEvent) -> None:
    msg = (
        "好欸！事新人！\n"
        f"在下 {choice(list(Config.BotSelfConfig.nickname))} 哒!w!"
    )
    await group_member_event.finish(msg)

@group_member_event.handle()
async def _gro(bot: Bot, event: GroupDecreaseNoticeEvent) -> None:
    if event.is_tome():
        msg = (
            "呜呜呜，主人"
            f"咱被群 {event.group_id} 里的 {event.operator_id} 扔出来了..."
        )
        for superuser in Config.BotSelfConfig.superusers:
            await sv.NetworkPost.send_private_msg(
                user_id=int(superuser),
                message=msg
            )
    else:
        await group_member_event.finish("阿！有人离开了我们...")


# 处理群管理事件
group_admin_event = sv.on_notice()

@group_admin_event.handle()
async def _group_admin_event(bot: Bot, event: GroupAdminNoticeEvent) -> None:
    if event.is_tome():
        return
    
    for superuser in Config.BotSelfConfig.superusers:
        await sv.NetworkPost.send_private_msg(
            user_id=int(superuser),
            message=f"好欸！主人！我在群 {event.group_id} 成为了管理！！"
        )


# 处理群禁言事件
group_ban_event = sv.on_notice()

@group_ban_event.handle()
async def _group_ban_event(bot: Bot, event: GroupBanNoticeEvent) -> None:
    if not event.is_tome():
        return
    
    if event.duration:
        msg = (
            "那个..。，主人\n"
            f"咱在群 {event.group_id} 被 {event.operator_id} 塞上了口球...\n"
            f"时长...是 {event.duration} 秒"
        )
        for superuser in Config.BotSelfConfig.superusers:
            await sv.NetworkPost.send_private_msg(
                user_id=int(superuser),
                message=msg
            )
    else:
        msg = (
            "好欸！主人\n"
            f"咱在群 {event.group_id} 被 {event.operator_id} 上的口球解除了！"
        )
        for superuser in Config.BotSelfConfig.superusers:
            await sv.NetworkPost.send_private_msg(
                user_id=int(superuser),
                message=msg
            )


# 处理群红包运气王事件
lucky_read_bag_event = sv.on_notice()

@lucky_read_bag_event.handle()
async def _lucky_read_bag_event(bot, event: LuckyKingNotifyEvent) -> None:
    msg = (
        "8行，这可忍？"
        f"gkd [CQ:at,qq={event.user_id}] 发一个！"
    )
    await lucky_read_bag_event.finish(Message(msg))


# 处理群文件上传事件
group_file_upload_event = sv.on_notice()

@group_file_upload_event.handle()
async def _group_file_upload_event(bot,
                                   event: GroupUploadNoticeEvent) -> None:
    await group_file_upload_event.finish("让我康康传了啥好东西")


# 处理撤回事件
recall_event = sv.on_notice()

@recall_event.handle()
async def _recall_event(bot: Bot, event: GroupRecallNoticeEvent) -> None:
    try:
        repo = await bot.get_msg(message_id=event.message_id)
    except:
        return
    
    group = event.group_id
    repo = str(repo["message"])
    check = await coolq_code_check(repo, group=group)
    if not check:
        repo = repo.replace("CQ", "QC")

    msg = (
        "主人，咱拿到了一条撤回信息！\n"
        f"{event.user_id}@[群:{event.group_id}]\n"
        "撤回了\n"
        f"{repo}"
    )

    for superuser in Config.BotSelfConfig.superusers:
        await sv.NetworkPost.send_private_msg(
            user_id=int(superuser),
            message=msg
        )

@recall_event.handle()
async def _rec(bot: Bot, event: FriendRecallNoticeEvent) -> None:
    try:
        repo = await bot.get_msg(message_id=event.message_id)
    except:
        return
    
    user = event.user_id
    repo = str(repo["message"])
    check = await coolq_code_check(repo, user)
    if not check:
        repo = repo.replace("CQ", "QC")

    msg = (
        "主人，咱拿到了一条撤回信息！\n"
        f"{event.user_id}@[私聊]"
        "撤回了\n"
        f"{repo}"
    )

    await bot.send(event, "咱看到惹~！")
    for superuser in Config.BotSelfConfig.superusers:
        await sv.NetworkPost.send_private_msg(
            user_id=int(superuser),
            message=msg
        )
