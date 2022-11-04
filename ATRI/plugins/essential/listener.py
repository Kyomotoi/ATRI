import json
from pathlib import Path

from nonebot.message import run_preprocessor
from nonebot.exception import IgnoredException
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent


__MANEGE_DIR = Path(".") / "data" / "plugins" / "manege"
__MANEGE_DIR.mkdir(parents=True, exist_ok=True)


# 检查用户是否存在于黑名单
@run_preprocessor
async def _(event: MessageEvent):
    blockuser_file_path = __MANEGE_DIR / "block_user.json"
    if not blockuser_file_path.is_file():
        with open(blockuser_file_path, "w", encoding="utf-8") as w:
            w.write(json.dumps(dict()))
    
    data = json.loads(blockuser_file_path.read_bytes())
    
    user_id = event.get_user_id()
    if user_id in data:
        raise IgnoredException(f"Blocked user: {user_id}")
    
    if isinstance(event, GroupMessageEvent):
        blockgroup_file_path = __MANEGE_DIR / "block_group.json"
        if not blockgroup_file_path.is_file():
            with open(blockgroup_file_path, "w", encoding="utf-8") as w:
                w.write(json.dumps(dict()))

        data = json.loads(blockgroup_file_path.read_bytes())
        
        group_id = str(event.group_id)
        if group_id in data:
            raise IgnoredException(f"Blocked group: {group_id}")


def init_listener():
    """初始化监听器"""
