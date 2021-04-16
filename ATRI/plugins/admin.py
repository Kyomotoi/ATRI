import json
import asyncio
from random import randint
from pathlib import Path

from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.adapters.cqhttp import (
    Bot,
    MessageEvent,
    GroupMessageEvent,
    PrivateMessageEvent
)
from nonebot.typing import T_State

from ATRI.config import Config
from ATRI.service import Service as sv
from ATRI.exceptions import load_error
from ATRI.utils.file import open_file


ESSENTIAL_DIR = Path('.') / 'ATRI' / 'data' / 'database' / 'essential'


__doc__ = """
好友申请处理
权限组：维护者
用法：
  /friendreq list
  /friendreq (y/n) reqid
补充:
  reqid: 申请码
"""

request_friend = sv.on_command(
    cmd="/friendreq",
    docs=__doc__,
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


__doc__ = """
群聊申请处理
权限组：维护者
用法：
  /groupreq list
  /groupreq (y/n) reqid
补充：
  reqid: 申请码
"""

request_group = sv.on_command(
    cmd="/groupreq",
    docs=__doc__,
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


__doc__ = """
广播
权限组：维护者
用法：
  /bc 内容
"""

broadcast = sv.on_command(
    cmd="/bc",
    docs=__doc__,
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
        await asyncio.sleep(randint(0, 2))
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


__doc__ = """
错误堆栈查看
权限组：维护者
用法：
  /track 追踪ID
"""

track_error = sv.on_command(
    cmd="/track",
    docs=__doc__,
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


__doc__ = """
获取控制台信息
权限组：维护者
用法：
  /getlog level line
补充：
  level: 等级(info, warning, error, debug)
  line: 行数(最近20行：-20)
"""

get_log = sv.on_command(
    cmd="/getlog",
    docs=__doc__,
    permission=SUPERUSER
)

@get_log.handle()
async def _get_log(bot: Bot, event: GroupMessageEvent) -> None:
    user = str(event.user_id)
    group = event.group_id
    node = []
    msg = str(event.message).split(" ")
    try:
        rows = msg[1]
    except:
        await get_log.finish("格式/gl level rows")
    
    if msg[0] == "info":
        level = "info"
    elif msg[0] == "warning":
        level = "warning"
    elif msg[0] == "error":
        level = "error"
    elif msg[0] == "debug":
        level = "debug"
    else:
        await get_log.finish("格式/gl level rows")
    
    path = LOGGER_DIR / level / f"{NOW_TIME}-INFO.log"  # type: ignore
    logs = await open_file(path, "readlines")
    
    try:
        content = logs[int(rows):]  # type: ignore
        repo = "\n".join(content).replace("[36mATRI[0m", "ATRI")
        node = [{
            "type": "node",
            "data": {"name": "ERROR REPO", "uin": user, "content": repo}
        }]
    except IndexError:
        await get_log.finish(f"行数错误...max: {len(logs)}")  # type: ignore
    
    await bot.send_group_forward_msg(group_id=group, messages=node)


__doc__ = """
紧急停机
权限组：维护者
用法：
  /down
"""

shutdown = sv.on_command(
    cmd="/down",
    docs=__doc__,
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
  /block (u,g) (int) (0,1)
补充：
  u：QQ
  g：QQ群
  int: 对应号码
  0,1：对应布尔值False, True
  范围为全局
示例：
  /block u 114514 1
  执行对QQ号为114514的封禁
"""

block = sv.on_command(
    cmd="/block",
    docs=__doc__,
    permission=SUPERUSER
)

@block.handle()
async def _block(bot: Bot, event: MessageEvent) -> None:
    msg = str(event.message).split(' ')
    _type = msg[0]
    arg = msg[1]
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
    /service 目标指令 u+uid,g+gid,global 0,1
  对于群管理：
    /service 目标指令 0,1
补充：
  user：QQ号
  group：QQ群号
  global：全局
  0,1：对应布尔值False, True
示例：
  对于维护者：
    /service /status u123456789 1
  对于群管理：
    /service /status 1
"""

service_control = sv.on_command(
    cmd='/service',
    docs=__doc__,
    permission=SUPERUSER|GROUP_OWNER|GROUP_ADMIN
)

@service_control.handle()
async def _service_control(bot: Bot, event: GroupMessageEvent) -> None:
    msg = str(event.message).split(' ')
    user = str(event.user_id)
    cmd = msg[0]
    _type = msg[1]
    
    if msg[0] == "":
        await service_control.finish('请检查输入~！')
    
    if user in Config.BotSelfConfig.superusers:
        is_enabled = int(msg[2])
        status = "启用" if bool(is_enabled) else "禁用"
        
        if _type == "global":
            sv.control_service(cmd, True, is_enabled)
            await service_control.finish(f"{cmd}已针对[{_type}]实行[{status}]")
        else:
            print(_type)
            if "u" in _type:
                qq = _type.replace('u', '')
                sv.control_service(cmd, False, is_enabled, user=qq)
            elif "g" in _type:
                group = _type.replace('g', '')
                sv.control_service(cmd, False, is_enabled, group=group)
            else:
                await service_control.finish("请检查输入~！")
            await service_control.finish(f"{cmd}已针对[{_type}]实行[{status}]")
    else:
        group = str(event.group_id)
        is_enabled = int(_type)
        sv.control_service(cmd, False, is_enabled, group=group)
        status = "启用" if bool(is_enabled) else "禁用"
        await service_control.finish(f"{cmd}已针对[{_type}]实行[{status}]")

@service_control.handle()
async def _serv(bot: Bot, event: PrivateMessageEvent) -> None:
    await service_control.finish("此功能仅在群聊中触发")


__doc__ = """
休眠bot，不处理任何信息
权限组：维护者
用法：
  /dormant (0,1)
补充：
  0,1: 对应布尔值(False,True)
"""

dormant = sv.on_command(
    cmd='/dormant',
    docs=__doc__,
    permission=SUPERUSER
)

@dormant.handle()
async def _dormant(bot: Bot, event: MessageEvent) -> None:
    msg = str(event.message).strip()
    if msg == "1":
        sv.Dormant.control_dormant(True)
        stat = "已进入休眠状态...期间咱不会回应任何人的消息哦..."
    else:
        sv.Dormant.control_dormant(False)
        stat = "唔...回复精神力！"
    await dormant.finish(stat)
