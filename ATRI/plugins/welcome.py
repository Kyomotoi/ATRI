import nonebot
from nonebot import on_notice
from nonebot.notice_request import NoticeSession, RequestSession
from nonebot.plugin import on_request
from nonebot.helpers import send_to_superusers

import config # type: ignore


bot = nonebot.get_bot()
master = config.MASTER()


@on_notice('group_increase')
async def _(session: NoticeSession):
    user = session.event.user_id
    me = session.event.self_id

    if user == me:
        await session.send('在下アトリ，今后请多指教呐❤')
    else:
        await session.send(f'[CQ:at,qq={user}]\nねえ❤...是新人欸！\nここでは遠慮はいらないのだからね❤')

@on_notice('group_decrease')
async def _(session: NoticeSession):
    user = session.event.user_id
    now = session.event.operator_id

    if now == user:
        inf = await bot.get_stranger_info(user_id = user) # type: ignore
        name = inf['nickname']
        await session.send(f'{name}({user}) 跑了......')


@on_request('friend_add')
async def _(session: RequestSession):
    user = session.event.user_id
    await send_to_superusers(bot, f'{user}\n想认识ATRI欸欸欸！！')

@on_request('group')
async def _(session: RequestSession):
    if session.event.user_id == master:
        await session.approve()
    else:
        await session.send(f'邀请入群请联系ATRI的主人[{master}]')