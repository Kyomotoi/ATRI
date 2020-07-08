# -*- coding:utf-8 -*-
import nonebot
from nonebot import on_command, CommandSession, permission as perm


bot = nonebot.get_bot()
master = bot.config.SUPERUSERS
bangroup = bot.config.bangroup


@on_command('关于', aliases=['关于', '关于机器人'], only_to_me=False)
async def _(session: CommandSession):
    await session.send('阿？想了解咱？\n写出咱的是Kyomotoi~\n他的主页:https://lolihub.icu\n项目地址:https://github.com/Kyomotoi/Aya')

@on_command('帮助', aliases=['帮助', '食用方法'], only_to_me=False)
async def _(session: CommandSession):
    await session.send('嗯...不会用咱的话，看这吧！https://lolihub.icu/#/robot/user')

@on_command('seach_this_group_p', aliases=['本群总人数', '总人数', '群人数'], only_to_me=False, permission=perm.GROUP)
async def _(session: CommandSession):
    try:
        seach_group_member = await session.bot.get_group_member_list(
            group_id=session.event.group_id
        )
    except:
        print('error')
        await session.send('获取数据时出问题，请重试')
        return
    
    await session.send(f'本群目前共有{len(seach_group_member)}人')

@on_command('send_all_group', aliases=['公告', '群发', '推送'], only_to_me=False)
async def send_all_group(session: CommandSession):
    if session.event.user_id in master:
        msg=session.current_arg.strip()
        if not msg:
            msg = session.get('message', prompt='请键入内容')
        group_list = await session.bot.get_group_list()
        for group in group_list:
            if group['group_id'] not in bangroup:
                try:
                    await bot.send_group_msg( group_id=group['group_id'], message=msg)
                except:
                    print('error')
                    pass
        await session.send('推送完成')