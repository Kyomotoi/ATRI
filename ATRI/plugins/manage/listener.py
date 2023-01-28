import json

from nonebot.matcher import Matcher
from nonebot.message import run_preprocessor
from nonebot.exception import IgnoredException
from nonebot.adapters.onebot.v11 import (
    MessageEvent,
    GroupMessageEvent,
    PrivateMessageEvent,
)

from ATRI.service import ServiceTools

from .data_source import MANAGE_DIR
from .plugin import *


@run_preprocessor
async def _(matcher: Matcher, event: MessageEvent):
    plugin_name = str(matcher.plugin_name)

    if not "nonebot_" in plugin_name:
        return
    
    if not "gocqhttp" in plugin_name:
        serv = ServiceTools(plugin_name)
        try:
            serv.load_service()
        except Exception:
            raise IgnoredException(f"{plugin_name} limited")

        if not serv.auth_service():
            raise IgnoredException(f"{plugin_name} limited")

        if isinstance(event, PrivateMessageEvent):
            user_id = event.get_user_id()
            result = serv.auth_service(user_id)
        elif isinstance(event, GroupMessageEvent):
            user_id = event.get_user_id()
            group_id = str(event.group_id)
            result = serv.auth_service(user_id, group_id)
        else:
            result = True

        if not result:
            raise IgnoredException(f"{plugin_name} limited")


@run_preprocessor
async def _(event: MessageEvent):
    blockuser_file_path = MANAGE_DIR / "block_user.json"
    if not blockuser_file_path.is_file():
        with open(blockuser_file_path, "w", encoding="utf-8") as w:
            w.write(json.dumps(dict()))

    data = json.loads(blockuser_file_path.read_bytes())

    user_id = event.get_user_id()
    if user_id in data:
        raise IgnoredException(f"Blocked user: {user_id}")

    if isinstance(event, GroupMessageEvent):
        blockgroup_file_path = MANAGE_DIR / "block_group.json"
        if not blockgroup_file_path.is_file():
            with open(blockgroup_file_path, "w", encoding="utf-8") as w:
                w.write(json.dumps(dict()))

        data = json.loads(blockgroup_file_path.read_bytes())

        group_id = str(event.group_id)
        if group_id in data:
            raise IgnoredException(f"Blocked group: {group_id}")


def init_listener():
    """初始化监听器"""
