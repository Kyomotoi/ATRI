import json
from pathlib import Path
from datetime import datetime

from nonebot.permission import SUPERUSER
from nonebot.plugin import on_command, on_message
from nonebot.adapters.cqhttp import (
    Bot,
    MessageEvent,
    GroupMessageEvent
)

from ATRI.exceptions import WriteError
from ATRI.log import logger


ADMIN_DIR = Path('.') / 'ATRI' / 'data' / 'database' / 'admin'


# 收集bot所在的群聊聊天记录
chat_monitor = on_message()

@chat_monitor.handle()
async def _chat_monitor(bot: Bot, event: GroupMessageEvent) -> None:
    now_time = datetime.now().strftime('%Y-%m-%d')
    file_name = f"{now_time}-chat.json"
    path = ADMIN_DIR / f"{event.group_id}" / file_name
    path.parent.mkdir(exist_ok=True, parents=True)
    path.parent.touch(exist_ok=True)
    
    try:
        data = json.loads(path.read_bytes())
    except FileExistsError:
        data = {}
    data[event.message_id] = {
        "post_type": event.post_type,
        "sub_type": event.sub_type,
        "user_id": event.user_id,
        "group_id": event.group_id,
        "message_type": event.message_type,
        "message": event.message,
        "raw_message": event.raw_message,
        "font": event.font,
        "sender": event.sender,
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
    

ESSENTIAL_DIR = Path('.') / 'ATRI' / 'data' / 'database' / 'essential'

request_friend = on_command(
    "好友申请",
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
    except FileExistsError:
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


request_group = on_command(
    "群聊申请",
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
