import json
from pathlib import Path
from datetime import datetime
from typing import Optional

from nonebot.plugin import on_command, on_message
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent

from ATRI.log import logger
from ATRI.rule import is_block
from ATRI.config import nonebot_config
from ATRI.utils.file import write_file
from ATRI.utils.apscheduler import scheduler
from ATRI.exceptions import WriteError


RUBBISH_DIR = Path('.') / 'ATRI' / 'data' / 'database' / 'anti-rubbish'
now_time = datetime.now().strftime('%Y%m%d-%H%M%S')


# 365 x 24 不间断监听啥b发屎人
# 日您🐎的，自己在厕所吃完自助餐还不够，还要分享给群友
# 👴就搁这公示公示这些啥b
# 每日0点如有发屎记录则全群通报
anti_rubbish = on_message()

@anti_rubbish.handle()
async def _anti_rubbish(bot: Bot, event: GroupMessageEvent) -> None:
    msg = str(event.message).strip()
    user = int(event.user_id)
    group = event.group_id
    key_word: dict = NoobRubbish.get_keyword()
    noob_data: dict = NoobRubbish.read_noobs(group)
    noob_data.setdefault(user, {})

    for key in key_word.keys():
        if key in msg:
            noob_data[user].setdefault(key, 1)
            noob_data[user][key] += 1
            await write_file(NoobRubbish._get_noob(group), json.dumps(noob_data))
            logger.info(
                f"GET 吃屎人 {user}[@群{group}] 第{noob_data[user][key]}次: {msg}")


rubbish = on_command("/rubbish", rule=is_block())

@rubbish.handle()
async def _rubbish(bot: Bot, event: GroupMessageEvent) -> None:
    cmd = str(event.message).split(" ")
    user = int(event.user_id)
    group = event.group_id
    
    if cmd[0] == "list":
        noob_data: dict = NoobRubbish.read_noobs(group)
        noob_list = ""
        for key in noob_data.keys():
            noob_list += f"{key}\n"
        
        if not noob_list:
            await rubbish.finish("此群很干净呢~！")
        else:
            msg = (
                f"截至{now_time}\n"
                f"吃过厕所自助餐的有：\n"
            ) + noob_list
            await rubbish.finish(msg)

    elif cmd[0] == "read":
        try:
            user = cmd[1]
        except:
            await rubbish.finish("格式/rubbish read qq")
        
        noob_data: dict = NoobRubbish.read_noob(group, int(user))
        if not noob_data:
            await rubbish.finish("该群友很干净！")
        else:
            noob_keys = ""
            for key in noob_data.keys():
                noob_keys += f"{key}-{noob_data[key]}次\n"
            msg = (
                f"截至{now_time}\n"
                f"此群友吃的屎的种类，以及次数：\n"
            ) + noob_keys
            await rubbish.finish(msg)
    
    elif cmd[0] == "update":
        if user not in nonebot_config["superusers"]:
            await rubbish.finish("没权限呢...")
        
        key_word = cmd[1]
        data = NoobRubbish.get_keyword()
        data[key_word] = now_time
        await NoobRubbish.store_keyword(data)
        await rubbish.finish(f"勉強しました！\n[{key_word}]")
    
    elif cmd[0] == "del":
        if user not in nonebot_config["superusers"]:
            await rubbish.finish("没权限呢...")
        
        key_word = cmd[1]
        data = NoobRubbish.get_keyword()
        del data[key_word]
        await NoobRubbish.store_keyword(data)
        await rubbish.finish(f"清除~！[{key_word}]")
    
    else:
        await rubbish.finish("请检查格式~！详细请查阅文档")


# @scheduler.scheduled_job(
#     "cron",
#     hour=0,
#     misfire_grace_time=120
# )
# async def _():
#     group = GroupMessageEvent.group_id
#     noob_data = NoobRubbish.read_noobs(group)


class NoobRubbish:
    @staticmethod
    def _get_noob(group: Optional[int] = None) -> Path:
        file_name = f"{now_time}.noob.json"
        GROUP_DIR = RUBBISH_DIR / f"{group}"
        path = GROUP_DIR / file_name
        
        if not GROUP_DIR.exists():
            GROUP_DIR.mkdir()
        return path
    
    @classmethod
    def read_noobs(cls, group: int) -> dict:
        try:
            data = json.loads(cls._get_noob(group).read_bytes())
        except:
            data = {}
        return data

    @classmethod
    def read_noob(cls, group: int, user: Optional[int]) -> dict:
        try:
            data = json.loads(cls._get_noob(group).read_bytes())
        except:
            data = {}
        data.setdefault(user, {})
        return data

    @staticmethod
    def get_keyword() -> dict:
        file_name = "keyword.json"
        path = RUBBISH_DIR / file_name
        try:
            data = json.loads(path.read_bytes())
        except:
            data = {}
        return data

    @staticmethod
    async def store_keyword(data: dict) -> None:
        file_name = "keyword.json"
        path = RUBBISH_DIR / file_name
        try:
            await write_file(path, json.dumps(data))
        except WriteError:
            raise WriteError("Writing file failed!")
