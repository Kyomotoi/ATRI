from nonebot import on_notice
from nonebot.plugin import on_request
from nonebot.notice_request import NoticeSession, RequestSession

import config
from ATRI.modules.funcControl import checkNoob


master = config.SUPERUSERS


@on_notice('group_increase')
async def _(session: NoticeSession):
    user = session.event.user_id
    group = session.event.group_id
    me = session.event.self_id

    if checkNoob(group):
        if user == me:
            await session.send('在下アトリ，今后请多指教呐❤')
        else:
            await session.send(f'[CQ:at,qq={user}]\nねえ❤...是新人欸！\nここでは遠慮はいらないのだからね❤')

@on_notice('group_decrease.leave')
async def _(session: NoticeSession):
    user = session.event.user_id
    group = session.event.group_id
    now = session.event.operator_id
    if checkNoob(user, group):
        if now == user:
            await session.send(f'[{user}]离开了我们......')


@on_request('friend', 'group.invite')
async def _(session: RequestSession):
    user = session.event.user_id
    if checkNoob(user):
        try:
            group = session.event.group_id
        except:
            group = False
        
        if group:
            await bot.send_private_msg(user_id = user, message = f'如有需要，请联系维护组{master}哦~') # type: ignore
            await bot.send_private_msg(user_id = master, message = f'报告主人！ATRI收到一条请求：\n类型：邀请入群\n邀请人：{user}\n对象群：{group}') # type: ignore
        
        else:
            await bot.send_private_msg(user_id = master, message = f'报告主人！ATRI收到一条请求：\n类型：添加好友\n申请人：{user}') # type: ignore