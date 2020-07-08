import nonebot
from nonebot import on_command, on_notice
from nonebot import CommandSession
from nonebot.notice_request import NoticeSession, RequestSession
from nonebot.plugin import on_request
from aiocqhttp.exceptions import ActionFailed

bot = nonebot.get_bot()
master = bot.config.SUPERUSERS


@on_notice('group_increase')
async def _(session: NoticeSession):
    q = session.event.user_id
    me = session.event.self_id

    if q == me :
        await session.send('在下綾，今后请多指教呐❤')
    else:
        await session.send(f'ねえ❤...是新人欸！\nここでは遠慮はいらないのだからね❤')

@on_notice('group_decrease')
async def _(session: NoticeSession):
    q = session.event.user_id
    qm = session.event.operator_id

    if qm == q:
        inf = await bot.get_stranger_info(user_id = q)

        name = inf['nickname']

        await session.send(f'ねえ...{name}({q}) 跑了...')

@on_notice('firend_add')
async def _(session: NoticeSession):
    u = session.event.user_id
    await bot.send_private_msg(self_id = session.self_id, user_id = u, message=f'有人来加我啦！\n{u}')


@on_request('group')
async def bot_request(session: RequestSession):
    g = session.event.group_id
    u = session.event.user_id
    mt = master[0]
    print(mt)

    if session.event.sub_type == 'invite':

        if welcome_switch:

            await session.bot.send_private_msg(self_id = session.self_id, user_id = u, message='你的请求吾辈已经告诉主人，请等待咱主人同意。\n作者联系方式：\nhttps://lolihub.icu/#/about')

            await session.bot.send_private_msg(self_id = session.self_id, user_id = mt, message=f'吾辈收到一个新邀请:\n裙: {g}\n邀请人: {u}\n是否同意(是 or 否)')

            @on_command('taowa', aliases=['是', '否'], only_to_me=False)
            async def _(session: CommandSession):
                waiting = session.event.raw_message.split(' ', 1)
                wait = waiting[0]

                if wait == '是':
                    try:
                        @on_request('group')
                        async def _(session: RequestSession):
                            await session.approve()
                    except ActionFailed as e:
                        print(e.retcode)

                    await session.bot.send_private_msg(self_id = session.self_id, user_id = mt, message='吾辈遵旨！')
                    
                    await session.bot.send_private_msg(self_id = session.self_id, user_id = u, message='你的请求已被吾辈的主人同意！')

                elif wait == '否':
                    await session.bot.send_private_msg(self_id = session.self_id, user_id = mt, message='吾辈已回应拒绝')

                    await session.bot.send_private_msg(self_id = session.self_id, user_id = u, message='你的请求已被吾辈的主人拒绝...')

        else:
            await session.bot.send_private_msg(self_id = session.self_id, user_id = u, message='主人告诉吾辈不能同意任何人的请求呢...\n作者联系方式：\nhttps://lolihub.icu/#/about')
            
            await session.bot.send_private_msg(self_id = session.self_id, user_id = mt, message=f'吾辈收到一个新的邀请请求，由于主人并未告知吾辈可以邀请，故做出拒绝的回应。\n邀请人: {u}')

welcome_switch = True
@on_command('welcome_switch', aliases=['开启', '关闭'], only_to_me=False)
async def _(session: CommandSession):
    if session.event.user_id in master:
        command = session.event.raw_message.split(' ', 1)
        switch = command[0]
        com = command[1]
        global welcome_switch
        if switch == '开启':
            if com == '邀请':
                welcome_switch = True
            else:
                pass

        elif switch == '关闭':
            if com == '邀请':
                welcome_switch = False
            else:
                pass
        
        await session.send('完成')
    
    else:
        await session.send('恁哪位?')