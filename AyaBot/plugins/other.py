import os
import random
from nonebot import on_command, CommandSession, permission as perm, on_request
from datetime import datetime
from typing import Optional

import pytz
from pandas import Timestamp


CST = 'Asia/Shanghai'

def get_beijing_time(freq: Optional[str] = None) -> datetime:
    now = datetime.now(pytz.timezone(CST))
    if freq is not None:
        now = Timestamp(now).round(freq)
    return now

def beijing_from_timestamp(timestamp: int) -> datetime:
    return datetime.fromtimestamp(timestamp, pytz.timezone(CST))


@on_command('阿这', only_to_me=False)
async def _(session: CommandSession):
    await session.send('阿这')

@on_command('喵', aliases=['喵喵', '喵喵喵'], only_to_me=False)
async def _(session: CommandSession):
    await session.send('喵~')

@on_command('奶宝', aliases=['@๑ ^ ₃•๑', '奶够翘'], only_to_me=False)
async def _(session: CommandSession):
    await session.send('别叫了别叫了，8在')

@on_command('抽签', only_to_me=False)
async def _(session: CommandSession):
    await session.send(str(random.choice(['大凶', '小凶', '凶', '吉', '小吉', '中吉', '大吉'])))

@on_command('掷骰子', aliases=['投骰子'], only_to_me=False)
async def _(session: CommandSession):
    await session.send(str(random.randint(1,6)))

@on_command('?', aliases=['？', '❓'], only_to_me=False)
async def _(session: CommandSession):
    await session.send('?')

@on_command('seach_this_group_p', aliases=['本群总人数', '总人数', '群人数'], only_to_me=False, permission=perm.GROUP)
async def _(session: CommandSession):
    try:
        seach_group_member = await session.bot.get_group_member_list(
            group_id=session.ctx['group_id']
        )
    except:
        await session.send('获取数据时出问题，请重试')
        return
    
    await session.send(f'本群目前共有{len(seach_group_member)}人')