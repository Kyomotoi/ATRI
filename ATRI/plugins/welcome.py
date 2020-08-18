import json
import nonebot
from pathlib import Path
from nonebot import on_notice
from nonebot.notice_request import NoticeSession, RequestSession
from nonebot.plugin import on_request
from aiocqhttp.exceptions import ActionFailed

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
    await bot.send_private_msg(
        user_id = master, # type: ignore
        message = f'{user}\n想认识ATRI欸欸欸！！'
    )

    with open(Path('.') / 'ATRI' / 'plugins' / 'switch' / 'switch.json', 'r') as f:
        data = json.load(f)
    
    if data["approve_friend_add"] == 0:
        try:
            await session.approve()
        except ActionFailed as e:
            print(e.retcode)
        await bot.send_private_msg(
            user_id = master, # type: ignore
            message = '由于主人已同意ATRI接近陌生人，故请求已同意！'
        )
        await bot.send_private_msg(
            user_id = user, # type: ignore
            message = f'初次见面，我是アトリ！咱可是高性能ですから~！\nATRI的使用方法（恁可少想有的没的8，老涩批）：https://lolihub.icu/#/robot/user'
        )

    else:
        await bot.send_private_msg(
            user_id = master, # type: ignore
            message = '由于主人不同意ATRI接近陌生人，故请求已回拒...'
        )
        await bot.send_private_msg(
            user_id = user, # type: ignore
            message = f'主人似乎不想让ATRI接触陌生人呢...'
        )

@on_request('group')
async def _(session: RequestSession):
    group = session.event.group_id
    user = session.event.user_id

    with open(Path('.') / 'ATRI' / 'plugins' / 'switch' / 'switch.json', 'r') as f:
        data = json.load(f)

    if session.event.sub_type == 'invite':

        if data["approve_invite_join_group"] == 0:
            await session.bot.send_private_msg(
                user_id = user, # type: ignore
                message = '嗯哼？想邀请ATRI入群嘛，正好！咱主人想让咱出去看看大世界！'
            )
            await session.bot.send_private_msg(
                user_id = master, # type: ignore
                message = f'ATRI收到一个新邀请:\n裙: {group}\n邀请人: {user}\n已同意'
            )

            try:
                await session.approve()
            except ActionFailed as e:
                print(e.retcode)

        else:
            await session.bot.send_private_msg(
                user_id = user, # type: ignore
                message = '主人告诉咱不能随便乱跑...\n作者联系方式：https://lolihub.icu/#/about'
            )
            await session.bot.send_private_msg(
                user_id = master, # type: ignore
                message = f'ATRI收到一个新邀请:裙: {group}\n邀请人: {user}\n已拒绝'
            )