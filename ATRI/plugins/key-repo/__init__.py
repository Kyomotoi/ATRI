import string
from datetime import datetime
from random import choice, sample

from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent

from ATRI.config import Config
from ATRI.service import Service as sv
from ATRI.utils.request import get_bytes
from ATRI.rule import is_in_service, to_bot

from .data_source import (
    add_history,
    add_key_temp,
    load_key_data,
    add_key,
    load_key_history,
    load_key_temp_data,
    del_key_temp
)


# 此功能暂未完善：未添加关键词删除

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#     ！屎山注意！屎山注意！屎山注意！屎山注意！
#          ！请自备降压药！请自备降压药！
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


__doc__ = """
涩涩的聊天（？
权限组：所有人
用法：
  @ (msg)
补充：
  @: at机器人
"""

keyrepo = sv.on_message(rule=is_in_service('keyrepo') & to_bot(), priority=5)
sv.manual_reg_service('keyrepo')

@keyrepo.handle()
async def _keyrepo(bot: Bot, event: MessageEvent) -> None:
    msg = str(event.get_message())
    data = load_key_data()

    for key in data.keys():
        if key in msg:
            await keyrepo.finish(choice(data[key]))


__doc__ = """
关键词申请/审核
（此功能未完善）
权限组：所有人
用法：
    /train add (key) (repo)
    对于维护者：
      /train list
      /train info (key)
      /train r (code) (0,1)
补充：
  key: 关键词
  repo: 回复
  0,1: 对应布尔值False/True
  code: 唯一识别码
示例：
  /train add hso 好涩哦
"""

train = sv.on_command(
    cmd="train",
    docs=__doc__
)

@train.handle()
async def _train(bot: Bot, event: GroupMessageEvent) -> None:
    user = event.user_id
    group = event.group_id
    
    msg = str(event.message).split(' ')
    _type = msg[0]
    code = "".join(sample(string.ascii_letters + string.digits, 10))
    
    if _type == "add":
        key = msg[1]
        args = msg[2]
        if user in Config.BotSelfConfig.superusers:
            add_key(key, args)
            msg = (
                "好欸学到了新的知识！\n"
                f"关键词：{key}\n"
                f"回复：{args}"
            )
            data = {
                "user": user,
                "group": group,
                "time": str(datetime.now()),
                "pass": True,
                "key": key,
                "repo": args,
                "feature": code
            }
            add_history(data)
            await train.finish(msg)
        else:
            data = {
                "user": user,
                "group": group,
                "time": str(datetime.now()),
                "pass": False,
                "key": key,
                "repo": args,
                "feature": code
            }
            add_key_temp(data)
            msg = (
                "感谢你的提交w，所提交的关键词将由维护者进行审核\n"
                f"识别码：{code}，你可以使用/train info 识别码\n"
                "以查询是否通过"
            )
            await train.finish(msg)
    elif _type == "list":
        data = load_key_temp_data()
        node = []
        for i in data:
            dic = {
                "type": "node",
                "data": {
                    "name": "idk",
                    "uin": i['user'],
                    "content": f"Key: {i['key']}\nRepo: {i['repo']}\nTime: {i['time']}"
                }
            }
            node.append(dic)
        if not node:
            node = [{
                "type": "node",
                "data": {
                    "name": "null",
                    "uin": str(user),
                    "content": "这里什么也没有呢..."
                }
            }]
        await bot.send_group_forward_msg(group_id=group, messages=node)
    elif _type == "info":
        key = msg[1]
        data = load_key_history()
        for i in data:
            if i['key'] == key:
                msg = (
                    f"{key} 审核信息:\n"
                    f"是否通过：{i['pass']}"
                    f"结果: K: {i['key']} | R: {i['repo']}\n"
                    f"来自：{i['user']}@[群:{i['group']}]\n"
                    f"申请时间：{i['time']}"
                )
                await train.finish(msg)
            else:
                await train.finish('未找到相关信息...')
    elif _type == "r":
        key = msg[1]
        args = int(msg[2])
        data = load_key_temp_data()
        if user in Config.BotSelfConfig.superusers:
            if args not in [0, 1]:
                await train.finish('请检查输入...')
            else:
                for i in data:
                    if bool(args):
                        if i['key'] == key:
                            msg = (
                                "好欸学到了新的知识！\n"
                                f"关键词：{i['key']}\n"
                                f"回复：{i['repo']}"
                            )
                            add_key(i['key'], i['repo'])
                            add_history(i)
                            await train.finish(msg)
                        else:
                            await train.finish('未找到相关信息...')
                    else:
                        add_history(i, False)
                        if del_key_temp(i):
                            await train.finish('已标记为不通过')
                        else:
                            await train.finish('未找到相关信息')
        else:
            await train.finish('不行哦~你的权限使得你没法这样做！')
    else:
        await train.finish('请检查输入...')
