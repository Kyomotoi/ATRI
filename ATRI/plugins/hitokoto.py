import json
from random import choice, randint
from nonebot.adapters.cqhttp import Bot, MessageEvent

from ATRI.rule import is_in_service, to_bot
from ATRI.service import Service as sv
from ATRI.exceptions import RequestError
from ATRI.utils.list import count_list, del_list_aim
from ATRI.utils.request import get_bytes

URL = [
    "https://cdn.jsdelivr.net/gh/hitokoto-osc/sentences-bundle@1.0.84/sentences/a.json",
    "https://cdn.jsdelivr.net/gh/hitokoto-osc/sentences-bundle@1.0.84/sentences/b.json",
    "https://cdn.jsdelivr.net/gh/hitokoto-osc/sentences-bundle@1.0.84/sentences/c.json",
]
sick_list = []


__doc__ = """
抑郁一下
权限组：所有人
用法：
  @ 一言
"""

hitokoto = sv.on_command(
    cmd="一言", aliases={"抑郁一下", "网抑云"}, docs=__doc__, rule=is_in_service("一言") & to_bot()
)


@hitokoto.handle()
async def _hitokoto(bot: Bot, event: MessageEvent) -> None:
    global sick_list
    msg = str(event.message)
    user = event.get_user_id()

    if count_list(sick_list, user) == 3:
        sick_list.append(user)
        await hitokoto.finish("额......需要咱安慰一下嘛~？")
    elif count_list(sick_list, user) == 6:
        sick_list = del_list_aim(sick_list, user)
        msg = "如果心里感到难受就赶快去睡觉！别再憋自己了！\n" "我...我会守在你身边的！...嗯..一定"
        await hitokoto.finish(msg)
    else:
        sick_list.append(user)
        url = choice(URL)
        try:
            data = json.loads(await get_bytes(url))
        except RequestError:
            raise RequestError("Request failed!")
        await hitokoto.finish(data[randint(1, len(data) - 1)]["hitokoto"])
