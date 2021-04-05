import os
import json
import time
from pathlib import Path
from datetime import datetime

from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import (
    Bot,
    MessageEvent,
    GroupMessageEvent
)
from nonebot.typing import T_State

from ATRI.config import Config
from ATRI.service import Service as sv
from ATRI.exceptions import WriteError, load_error
from ATRI.utils.file import open_file
from ATRI.log import (
    logger,
    LOGGER_DIR,
    NOW_TIME
)


ADMIN_DIR = Path('.') / 'ATRI' / 'data' / 'database' / 'admin'
os.makedirs(ADMIN_DIR, exist_ok=True)


# 收集bot所在的群聊聊天记录
chat_monitor = sv.on_message()

@chat_monitor.handle()
async def _chat_monitor(bot: Bot, event: GroupMessageEvent) -> None:
    now_time = datetime.now().strftime('%Y-%m-%d')    
    GROUP_DIR = ADMIN_DIR / f"{event.group_id}"
    path = GROUP_DIR / f"{now_time}.chat.json"
    now_time = datetime.now().strftime('%Y%m%d-%H%M%S')
    
    if not GROUP_DIR.exists():
        GROUP_DIR.mkdir()
    
    try:
        data = json.loads(path.read_bytes())
    except:
        data = {}
    data[event.message_id] = {
        "date": now_time,
        "time": time.time(),
        "post_type": event.post_type,
        "sub_type": event.sub_type,
        "user_id": event.user_id,
        "group_id": event.group_id,
        "message_type": event.message_type,
        "message": event.message.__str__(),
        "raw_message": event.raw_message,
        "font": event.font,
        "sender": {
            "user_id": event.sender.user_id,
            "nickname": event.sender.nickname,
            "sex": event.sender.sex,
            "age": event.sender.age,
            "card": event.sender.card,
            "area": event.sender.area,
            "level": event.sender.level,
            "role": event.sender.role,
            "title": event.sender.title
        },
        "to_me": event.to_me
    }
    try:
        with open(path, 'w', encoding='utf-8') as r:
            r.write(
                json.dumps(
                    data, indent=4
                )
            )
        logger.debug(f"写入消息成功，id: {event.message_id}")
    except WriteError:
        logger.error("消息记录失败，可能是缺少文件的原因！")
    else:
        pass


ESSENTIAL_DIR = Path('.') / 'ATRI' / 'data' / 'database' / 'essential'

request_friend = sv.on_command(
    cmd="好友申请",
    docs="好友申请处理",
    permission=SUPERUSER
)

@request_friend.handle()
async def _request_friend(bot: Bot, event: MessageEvent) -> None:
    msg = str(event.message).split(" ")
    key = msg[0]
    data = {}
    path = ESSENTIAL_DIR / "request_friend.json"
    try:
        data = json.loads(path.read_bytes())
    except:
        await request_friend.finish("读取数据失败，可能并没有请求...")
    
    if key == "list":
        msg0 = ""
        for i in data.keys():
            msg0 += f"{i} | {data[i]['user_id']} | {data[i]['comment']}\n"
        
        msg = "好友申请列表如下：\n"
        msg += msg0
        await request_friend.finish(msg)
    
    elif key == "y":
        arg = msg[1]
        await bot.set_friend_add_request(flag=arg, approve=True)
        await request_friend.finish(f"完成~！已同意 {data[arg]['user_id']} 的申请")
    
    elif key == "n":
        arg = msg[1]
        await bot.set_friend_add_request(flag=arg, approve=False)
        await request_friend.finish(f"完成~！已拒绝 {data[arg]['user_id']} 的申请")
    
    else:
        await request_friend.finish("阿...请检查输入——！")


request_group = sv.on_command(
    cmd="群聊申请",
    docs="群聊申请处理",
    permission=SUPERUSER
)

@request_group.handle()
async def _request_group(bot: Bot, event: MessageEvent) -> None:
    msg = str(event.message).split(" ")
    key = msg[0]
    data = {}
    path = ESSENTIAL_DIR / "request_group.json"
    try:
        data = json.loads(path.read_bytes())
    except FileExistsError:
        await request_friend.finish("读取数据失败，可能并没有请求...")
    
    if key == "list":
        msg0 = ""
        for i in data.keys():
            msg0 += f"{i} | {data[i]['sub_type']} | {data[i]['user_id']} | {data[i]['comment']}\n"
        
        msg = "群申请列表如下：\n"
        msg += msg0
        await request_friend.finish(msg)
    
    elif key == "y":
        arg = msg[1]
        try:
            await bot.set_group_add_request(flag=arg,
                                            sub_type=data[arg]['sub_type'],
                                            approve=False)
            await request_friend.finish(f"完成~！已同意 {data[arg]['user_id']} 的申请")
        except:
            await request_friend.finish("请检查输入的值是否正确——！")
    
    elif key == "n":
        arg = msg[1]
        try:
            await bot.set_group_add_request(flag=arg,
                                            sub_type=data[arg]['sub_type'],
                                            approve=False)
            await request_friend.finish(f"完成~！已拒绝 {data[arg]['user_id']} 的申请")
        except:
            await request_friend.finish("请检查输入的值是否正确——！")
    
    else:
        await request_friend.finish("阿...请检查输入——！")


broadcast = sv.on_command(
    cmd="/bc",
    docs="广播\n用法：/bc 广播内容",
    permission=SUPERUSER
)

@broadcast.handle()
async def _broadcast(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    if msg:
        state["msg"] = msg
    
@broadcast.got("msg", prompt="请告诉咱需要群发的内容~！")
async def _bd(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = state["msg"]
    group_list = await bot.get_group_list()
    succ_list = []
    err_list = []
    
    for group in group_list:
        try:
            await bot.send_group_msg(group_id=group["group_id"],
                                     message=msg)
        except:
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


track_error = sv.on_command(
    cmd="/track",
    docs="报错堆栈查看\n用法：/track 追踪ID",
    permission=SUPERUSER
)

@track_error.handle()
async def _track_error(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    if msg:
        state["msg"] = msg

@track_error.got("msg", prompt="请告诉咱追踪ID！")
async def _(bot: Bot, event: MessageEvent, state: T_State) -> None:
    track_id = state["msg"]
    data = {}
    
    try:
        data = load_error(track_id)
    except:
        await track_error.finish("Ignore track ID!")
    
    msg0 = (
        f"ID: {track_id}\n"
        f"Time: {data['time']}\n"
        f"Prompt: {data['prompt']}\n"
        f"{data['content']}"
    )
    
    await track_error.finish(msg0)


get_log = sv.on_command(
    cmd="/getlog",
    docs="获取控制台信息\n用法：/getlog 等级：info,warning,debug 行数：比如-20即最近20行",
    permission=SUPERUSER
)

@get_log.handle()
async def _get_log(bot: Bot, event: MessageEvent) -> None:
    msg = str(event.message).split(" ")
    try:
        rows = msg[1]
    except:
        await get_log.finish("格式/getlog level rows")
    
    if msg[0] == "info":
        level = "info"
    elif msg[0] == "warning":
        level = "warning"
    elif msg[0] == "error":
        level = "error"
    elif msg[0] == "debug":
        level = "debug"
    else:
        await get_log.finish("格式/getlog level rows")
    
    path = LOGGER_DIR / level / f"{NOW_TIME}-INFO.log"  # type: ignore
    logs = await open_file(path, "readlines")
    
    try:
        content = logs[int(rows):]  # type: ignore
    except IndexError:
        await get_log.finish(f"行数错误...max: {len(logs)}")  # type: ignore
    
    await get_log.finish("\n".join(content).replace("[36mATRI[0m", "ATRI"))  # type: ignore


shutdown = sv.on_command(
    cmd="/st",
    docs="紧急停机",
    permission=SUPERUSER
)

@shutdown.handle()
async def _shutdown(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    if msg:
        state["msg"] = msg

@shutdown.got("msg", prompt="WARNING，此项操作将强行终止bot运行，是否继续(y/n)")
async def __shutdown(bot: Bot, event: MessageEvent, state: T_State) -> None:
    if state["msg"] == "y":
        await bot.send(event, "咱还会醒来的，一定")
        exit(0)
    else:
        await shutdown.finish("再考虑下先吧 ;w;")


__doc__ = """
懒得和你废话，block了
权限组：维护者
用法：
  /b user,group 0,1
补充：
  user：QQ号
  group：QQ群号
  0,1：对应布尔值False, True
  范围为全局
"""

block = sv.on_command(
    cmd="/b",
    docs="懒得和你废话，block了\n用法：/b u,g 0,1",
    permission=SUPERUSER
)

@block.handle()
async def _block(bot: Bot, event: MessageEvent) -> None:
    msg = str(event.message).split(' ')
    _type = msg[0]
    arg = int(msg[1])
    is_enabled = bool(int(msg[2]))
    b_type = ""
    
    status = "封禁" if is_enabled else "解封"
    
    if _type == "g":
        sv.BlockSystem.control_list(is_enabled=is_enabled, group=arg)
        b_type = "Group"
    elif _type == "u":
        sv.BlockSystem.control_list(is_enabled, user=arg)
        b_type = "User"
    else:
        await block.finish("请检查输入...")

    await block.finish(f"已成功将[{b_type}@{arg}]{status}")


__doc__ = """
功能开关控制
权限组：维护者，群管理
用法：
  对于维护者：
    /s 目标指令 u+int,g+int,global 0,1
  对于群管理：
    /s 目标指令 0,1
补充：
  user：QQ号
  group：QQ群号
  global：全局
  0,1：对应布尔值False, True
示例：
  对于维护者：
    /s /status u123456789 0
  对于群管理：
    /s /status 0
"""

service_control = sv.on_command(
    cmd="/s",
    docs=__doc__,
    permission=SUPERUSER
)

@service_control.handle()
async def _service_control(bot: Bot, event: MessageEvent) -> None:
    msg = str(event.message).split(' ')
    user = event.user_id
    cmd = msg[0]
    _type = msg[1]
    is_enabled = bool(msg[2])
    
    status = "封禁" if is_enabled else "解封"
    
    if user in Config.BotSelfConfig.superusers:
        if _type == "global":
            sv.control_service(cmd, True, is_enabled)
        else:
            if "u" in _type:
                qq = _type.replace('u', '')
                sv.control_service(cmd, False, is_enabled, user=int(qq))
            elif "g" in _type:
                group = _type.replace('g', '')
                sv.control_service(cmd, False, is_enabled, group=int(group))
            else:
                await service_control.finish("请检查输入~！")
    else:
        if isinstance(event, GroupMessageEvent):
            group = event.group_id
            sv.control_service(cmd, False, bool(_type), group=group)
        else:
            await service_control.finish("此功能仅在群聊中触发")
    
    await service_control.finish(f"{cmd}已针对[{_type}]实行[{status}]")