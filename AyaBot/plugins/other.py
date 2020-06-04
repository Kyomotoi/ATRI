import os
import random
import nonebot
from nonebot import on_command, CommandSession, permission as perm, on_request


bot = nonebot.get_bot()
master = bot.config.SUPERUSERS
bangroup = [] #推送屏蔽群名单



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

@on_command('send_all_group', aliases=['公告', '群发', '推送'], only_to_me=False)
async def send_all_group(session: CommandSession):
    if session.ctx['user_id'] in master:
        msg=session.current_arg.strip()
        if not msg:
            msg = session.get('message', prompt='请键入内容')
        group_list = await session.bot.get_group_list()
        for group in group_list:
            if group['group_id'] not in bangroup:
                try:
                    await bot.send_group_msg( group_id=group['group_id'], message='ADMIN推送:\n' + msg)
                except:
                    pass
        await session.send('推送完成')