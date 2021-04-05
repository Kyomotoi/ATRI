import asyncio
from pathlib import Path
from random import choice, randint

from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent
from nonebot.adapters.cqhttp.message import Message

from ATRI.service import Service as sv
from ATRI.utils.limit import is_too_exciting
from ATRI.rule import (
    is_block,
    is_in_dormant,
    is_in_service
)


__doc__ = """
看不懂的笑话
权限组：所有人
用法：
  来句笑话
"""

get_laugh = sv.on_command(
    cmd="来句笑话",
    docs=__doc__,
    rule=is_block() & is_in_dormant()
    & is_in_service('来句笑话')
)

@get_laugh.handle()
async def _get_laugh(bot: Bot, event: MessageEvent) -> None:
    user_name = event.sender.nickname
    laugh_list = []
    
    FILE = Path('.') / 'ATRI' / 'data' / 'database' / 'funny' / 'laugh.txt'
    with open(FILE, 'r', encoding='utf-8') as r:
        for line in r:
            laugh_list.append(line.strip('\n'))
    
    result = choice(laugh_list)
    await get_laugh.finish(result.replace("%name", user_name))


me_to_you = sv.on_message(
    rule=is_block() & is_in_dormant() & is_in_service('你又行了')
)
sv.manual_reg_service('你又行了')

@me_to_you.handle()
async def _me_to_you(bot: Bot, event: MessageEvent) -> None:
    if randint(0, 5) == 5:
        msg = str(event.message)
        if "我" in msg and "CQ" not in msg:
            await me_to_you.finish(msg.replace("我", "你"))


__doc__ = """
随机选择一位群友成为我的老婆！
权限组：所有人
用法：
  抽老婆
"""

roll_wife = sv.on_command(
    cmd="抽老婆",
    docs=__doc__,
    rule=is_block() & is_in_dormant() & is_in_service('抽老婆')
)

@roll_wife.handle()
async def _roll_wife(bot: Bot, event: GroupMessageEvent) -> None:
    user = event.user_id
    group = event.group_id
    user_name = await bot.get_group_member_info(group_id=group,
                                                user_id=user)
    user_name = user_name['nickname']
    run = await is_too_exciting(user, group, 5, True)
    if not run:
        return
    
    luck_list = await bot.get_group_member_list(group_id=group)
    luck_user = choice(luck_list)
    luck_qq = luck_user['user_id']
    luck_user = luck_user['nickname']
    msg = (
        "5秒后咱将随机抽取一位群友成为\n"
        f"{user_name} 的老婆！究竟是谁呢~？"
    )
    await bot.send(event, msg)
    await asyncio.sleep(5)
    msg = (
        f"> {luck_user}({luck_qq})\n"
        f"恭喜成为 {user_name} 的老婆~⭐"
    )
    await bot.send(event, msg)


__doc__ = """
伪造转发
权限组：所有人
用法：
  /fm qq-name-msg...
补充:
  qq: QQ号
  name: 消息中的ID
  msg: 对应信息
示例:
  /fm 123456789*生草人*草 114514*仙贝*臭死了
"""

fake_msg = sv.on_command(
    cmd="/fm",
    docs=__doc__,
    rule=is_block() & is_in_service('/fm') & is_in_dormant()
)

@fake_msg.handle()
async def _fake_msg(bot: Bot, event: GroupMessageEvent) -> None:
    msg = str(event.message).split(' ')
    user = event.user_id
    group = event.group_id
    node = []
    check = await is_too_exciting(user, group, 2, True)
    
    if check:
        for i in msg:
            args = i.split('*')
            print(args)
            qq = args[0]
            name = args[1].replace('&#91;', '[')
            name = name.replace('&#93;', ']')
            repo = args[2].replace('&#91;', '[')
            repo = repo.replace('&#93;', ']')
            dic = {
                "type": "node",
                "data": {
                    "name": name,
                    "uin": qq,
                    "content": repo
                }
            }
            node.append(dic)
    await bot.send_group_forward_msg(group_id=group, messages=node)
