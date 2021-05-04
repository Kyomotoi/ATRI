import re
import asyncio
from random import choice

from nonebot.typing import T_State
from nonebot.adapters.cqhttp import (
    Bot,
    MessageEvent,
    GroupMessageEvent,
    PrivateMessageEvent,
)

from ATRI.service import Service as sv
from ATRI.rule import is_in_service
from ATRI.utils.limit import is_too_exciting

from .data_source import Tsuma


__doc__ = """
好欸！是老婆！
权限组：所有人
用法：
  抽老婆  # 获取一位老婆
  查老婆  # 查询老婆，如+at对象可查询对方
  我要离婚  # 离婚...
"""

roll_wife = sv.on_command(cmd="抽老婆", docs=__doc__, rule=is_in_service("抽老婆"))


@roll_wife.handle()
async def _roll_wife(bot: Bot, event: GroupMessageEvent) -> None:
    user = event.user_id
    gender = event.sender.sex
    group = event.group_id
    user_name = await bot.get_group_member_info(group_id=group, user_id=user)
    user_name = user_name["nickname"]
    run = is_too_exciting(user, 1, seconds=5)
    if not run:
        return

    check_repo, if_h = Tsuma.check_tsuma(str(user))
    if if_h:
        await roll_wife.finish(check_repo)

    msg = "5秒后咱将随机抽取一位群友成为\n" f"{user_name} 的老婆！究竟是谁呢~？"
    await bot.send(event, msg)
    await asyncio.sleep(5)

    async def get_luck_user():
        luck_list = await bot.get_group_member_list(group_id=group)
        return choice(luck_list)

    while True:
        luck_user = await get_luck_user()
        luck_qq = luck_user["user_id"]
        if user != luck_qq:
            break

    luck_gender = luck_user["sex"]
    luck_user = luck_user["nickname"]
    d = {
        "nickname": user_name,
        "gender": gender,
        "lassie": {"nickname": luck_user, "qq": luck_qq, "gender": luck_gender},
    }

    if str(luck_qq) == str(event.self_id):
        Tsuma.got_tsuma(str(user), d)
        msg = "老婆竟是我自己~❤"
    else:
        msg = Tsuma.got_tsuma(str(user), d)

    await roll_wife.finish(msg)


@roll_wife.handle()
async def _no_pr(bot: Bot, event: PrivateMessageEvent) -> None:
    await roll_wife.finish("对8起...该功能只对群聊开放（")


inquire_wife = sv.on_command(cmd="查老婆", rule=is_in_service("抽老婆"))


@inquire_wife.handle()
async def _inq_wife(bot: Bot, event: MessageEvent) -> None:
    msg = str(event.message).split(" ")
    if msg[0] == "":
        user = str(event.user_id)
        await inquire_wife.finish(Tsuma.inquire_tsuma(user))
    else:
        aim = re.findall(r"qq=(.*?)]", msg[0])[0]
        await inquire_wife.finish(Tsuma.inquire_tsuma(aim).replace("你", "ta"))


want_divorce = sv.on_command(cmd="我要离婚", rule=is_in_service("抽老婆"))


@want_divorce.handle()
async def _want_div(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    if msg:
        state["is_d"] = msg


@want_divorce.got("is_d", prompt="你确定吗？(是/否)")
async def _deal_div(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = state["is_d"]
    user = str(event.user_id)
    name = event.sender.nickname

    if msg in ["是", "确定"]:
        await want_divorce.finish(Tsuma.divorce(user))
    else:
        await want_divorce.finish(f"({name})回心转意了！")
