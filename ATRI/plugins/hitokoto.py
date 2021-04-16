import os
import json
from pathlib import Path
from random import choice, randint
from nonebot.adapters.cqhttp import Bot, MessageEvent

from ATRI.rule import is_in_service, to_bot
from ATRI.service import Service as sv
from ATRI.exceptions import LoadingError
from ATRI.utils.list import count_list, del_list_aim


HITOKOTO_DIR = Path('.') / 'ATRI' / 'data' / 'database' / 'hitokoto'
sick_list = []


__doc__ = """
抑郁一下
权限组：所有人
用法：
  @一言
  @抑郁一下
  @网抑云
补充：
  @：at Bot
"""

hitokoto = sv.on_command(
    cmd='一言',
    docs=__doc__,
    rule=is_in_service('一言')
)

@hitokoto.handle()
async def _hitokoto(bot: Bot, event: MessageEvent) -> None:
    global sick_list
    msg = str(event.message)
    user = event.get_user_id()
    hito_key = ['一言', '抑郁一下', '网抑云']
    
    if msg not in hito_key:
        return

    if count_list(sick_list, user) == 3:
        sick_list.append(user)
        await hitokoto.finish("额......需要咱安慰一下嘛~？")
    elif count_list(sick_list, user) == 6:
        sick_list = del_list_aim(sick_list, user)
        msg = (
            "如果心里感到难受就赶快去睡觉！别再憋自己了！\n"
            "我...我会守在你身边的！...嗯..一定"
        )
        await hitokoto.finish(msg)
    else:
        sick_list.append(user)
        rd = choice(os.listdir(HITOKOTO_DIR))
        path = HITOKOTO_DIR / rd
        data = {}
        try:
            data = json.loads(path.read_bytes())
        except LoadingError:
            raise LoadingError("Loading error!")
        await hitokoto.finish(data[randint(1, len(data) - 1)]['hitokoto'])
