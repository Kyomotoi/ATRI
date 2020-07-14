# -*- coding:utf-8 -*-
import nonebot
from nonebot import on_command, CommandSession


bot = nonebot.get_bot()
master = bot.config.SUPERUSERS
ban_group = bot.config.BANGROUP


@on_command('send_all_group', aliases=['公告', '群发', '推送'], only_to_me=False)
async def send_all_group(session: CommandSession):
    if session.event.user_id in master:
        msg = session.current_arg.strip()

        if not msg:
            msg = session.get('message', prompt='请告诉吾辈需要群发的内容~！')

        group_list = await session.bot.get_group_list()

        for group in group_list:

            if group['group_id'] not in ban_group:

                try:
                    await bot.send_group_msg(group_id = group['group_id'], message = msg)

                except:
                    pass

        await session.send('吾辈推送...完成！')


@on_command('send_to_group', aliases=['对群'], only_to_me=False)
async def send_to_group(session: CommandSession):
    if session.event.user_id in master:
        msg = session.current_arg.strip()
    
        if not msg:
            msg = session.get('message', prompt='请告诉吾辈完整内容呢...\n例：对群 12345647(群号) message')
        
        lg = msg.split(' ')

        group = lg[0]
        msg = lg[1]
        rei = lg[2]
        
        if rei:
            for i in range(1, int(rei)):
                try:
                    await bot.send_group_msg(group_id = group, message = msg)
                except:
                    await session.send('发送失败，请重试')
        
        else:
            await session.send('吾辈推送...完成！')

            try:
                await bot.send_group_msg(group_id = group, message = msg)
            except:
                await session.send('发送失败，请重试')
        
        await session.send('吾辈推送...完成！')


@on_command('send_to_qq', aliases=['对QQ'], only_to_me=False)
async def send_to_qq(session: CommandSession):
    if session.event.user_id in master:
        msg = session.current_arg.strip()
    
        if not msg:
            msg = session.get('message', prompt='请告诉吾辈完整内容呢...\n例：对QQ 12345647(QQ号) message')
        
        lg = msg.split(' ')

        qq = lg[0]
        msg = lg[1]

        try:
            await bot.send_private_msg(user_id = qq, message = msg)
        except:
            await session.send('发送失败，请重试')
        
        await session.send('吾辈推送...完成！')
