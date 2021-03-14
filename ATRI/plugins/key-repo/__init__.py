import os
import json
import time
from random import choice
from pathlib import Path

from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent

from ATRI.config import nonebot_config
from ATRI.service import Service as sv
from ATRI.rule import is_block, is_in_dormant, is_in_service, to_bot


# 此功能未完善


KEYREPO_DIV = Path('.') / 'ATRI' / 'data' / 'database' / 'KeyRepo'
os.makedirs(KEYREPO_DIV, exist_ok=True)


__plugin_name__ = "KeyRepo"

keyrepo = sv.on_message(rule=is_block()
                        & is_in_dormant()
                        & is_in_service(__plugin_name__)
                        & to_bot())

@keyrepo.handle()
async def _keyrepo(bot: Bot, event: MessageEvent) -> None:
    msg = str(event.get_message())

    file_name = "data.json"
    path = KEYREPO_DIV / file_name
    try:
        data = json.loads(path.read_bytes())
    except:
        with open(path, 'w') as r:
            r.write(json.dumps({}))
        data = {}

    for key in data.keys():
        if key in msg:
            await keyrepo.finish(choice(data[key]))


train = sv.on_command(
    name="调教",
    cmd="/train",
    rule=is_block()
)

@train.got("key", prompt="哦哦哦要开始学习了！请告诉咱知识点")
async def _train(bot: Bot, event: MessageEvent, state: T_State) -> None:
    if "[CQ" in state["key"]:
        await train.reject("仅支持纯文本呢...")

@train.got("repo", prompt="咱该如何回答呢？")
async def _trainR(bot: Bot, event: MessageEvent, state: T_State) -> None:
    if "[CQ" in state["repo"]:
        await train.reject("仅支持纯文本呢...")
        
    if state["key"] == "-d":
        file_name = "review.json"
        path = KEYREPO_DIV / file_name
        try:
            data = json.loads(path.read_bytes())
        except:
            data = {}

        key = state["repo"]
        if key not in data:
            await train.finish("未发现该待审核的知识点呢...")
        else:
            msg = (
                f"Key: {key}\n"
                f"Repo: {data[key]['repo']}\n"
                "已经从咱的审核列表移除！"
            )
            del data[key]
            with open(path, 'w') as r:
                r.write(json.dumps(data))
            await train.finish(msg)
    elif state["key"] == "-i":
        file_name = "review.json"
        path = KEYREPO_DIV / file_name
        try:
            data = json.loads(path.read_bytes())
        except:
            data = {}
        if state["repo"] not in data:
            await train.finish("未发现该知识点呢")
        key = data[state["repo"]]
        
        msg = (
            f"用户: {key['user']}\n"
            f"知识点: {state['repo']}"
            f"回复: {key['repo']}"
            f"时间: {key['time']}"
            "/train -r 知识点 y/n"
        )
        await train.finish(msg)
    elif state["key"] == "-ls":
        file_name = "review.json"
        path = KEYREPO_DIV / file_name
        try:
            data = json.loads(path.read_bytes())
        except:
            data = {}
        keys = "，".join(data.keys())
        msg = f"目前等待审核的有如下：\n{keys}"
        await train.finish(msg)
    elif state["key"] == "-r":
        file_name = "review.json"
        path = KEYREPO_DIV / file_name
        try:
            data = json.loads(path.read_bytes())
        except:
            data = {}
        
    
    key = state["key"]
    repo = state["repo"]
    user = event.get_user_id()
    if user not in nonebot_config["superusers"]:
        file_name = "review.json"
        path = KEYREPO_DIV / file_name
        try:
            data = json.loads(path.read_bytes())
        except:
            data = {}
        
        if key in data:
            msg = "欸欸欸，该词还在等待咱的审核，请先等先来的审核完再提交吧..."
            await train.finish(msg)
        else:
            data[key] = {
                "user": user,
                "repo": repo,
                "time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            }
            with open(path, 'r') as r:
                r.write(json.dumps(data, indent=4))

            msg = (
            "欸欸欸这不错欸！不过，还是先等待咱审核审核，"
            "如想撤销本次学习，请发送 /train -d 知识点"
            )
            await train.finish(msg)
        
    else:
        file_name = "data.json"
        path = KEYREPO_DIV / file_name
        try:
            data = json.loads(path.read_bytes())
        except:
            data = {}
        
        if key in data:
            repo_list: list = data[key]
            repo_list.append(repo)
            data[key] = repo_list
            msg = f"哦哦哦，{key}原来还有这样的回复，学到了~！"
            await bot.send(event, msg)
        else:
            data[key] = [repo]
            msg = "好欸，咱学到了新的知识点！"
            await bot.send(event, msg)
        
        with open(path, 'w') as r:
            r.write(json.dumps(data))
