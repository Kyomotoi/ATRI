import time
import json
from pathlib import Path
import nonebot
from nonebot.helpers import send_to_superusers
from nonebot import on_command, CommandSession

import config


bot = nonebot.get_bot()
master = config.SUPERUSERS


@on_command('send_all_group', aliases = ['公告', '群发', '推送'], only_to_me=False)
async def send_all_group(session: CommandSession):
    if session.event.user_id in master:
        msg = session.current_arg.strip()

        start = time.perf_counter()

        try:
            with open(Path('.') / 'ATRI' / 'plugins' / 'noobList' / 'noobGroup.json', 'r') as f:
                data = json.load(f)
        except:
            data = {}

        ban_group = list(data.keys())

        if not msg:
            msg = session.get('message', prompt='请告诉吾辈需要群发的内容~！')

        group_list = await session.bot.get_group_list() # type: ignore
        g_list = len(group_list)

        for group in group_list:

            if group['group_id'] not in ban_group:

                try:
                    await bot.send_group_msg(group_id = group['group_id'], message = msg) # type: ignore

                except:
                    pass
        
        end = time.perf_counter()

        await session.send(f'已推送到[{g_list}]个群\n耗时：{round(end - start, 3)}')

# @on_command('send_to_group', aliases=['对群'], only_to_me=False)
# async def send_to_group(session: CommandSession):
#     if session.event.user_id in master:
#         msg = session.current_arg.strip()
    
#         if not msg:
#             msg = session.get('message', prompt='请告诉吾辈完整内容呢...\n例：对群 12345647(群号) message 1')
        
#         lg = msg.split(' ')

#         group = lg[0]
#         msg = lg[1]
#         rei = 1 
#         try:
#             rei = int(lg[2]) + 1
#         except:
#             pass

#         if rei:
#             for i in range(1, rei):
#                 try:
#                     await bot.send_group_msg(group_id = group, message = msg) # type: ignore
#                 except:
#                     await session.send('发送失败，请重试')
        
#         else:
#             try:
#                 await bot.send_group_msg(group_id = group, message = msg) # type: ignore
#             except:
#                 await session.send('发送失败，请重试')
        
#         await session.send('推送完成！')


@on_command('send_all_friend', aliases = ['全体用户'], only_to_me = False)
async def send_all_friend(session: CommandSession):
    if session.event.user_id in master:
        msg = session.current_arg.strip()

        start = time.perf_counter()

        if not msg:
            msg = session.get('message', prompt='请告诉吾辈需要群发的内容~！')
        
        friend_list = await session.bot.get_friend_list() # type: ignore
        print(friend_list)
        f_list = len(friend_list)
        try:
            await send_all_friend(user_id = friend['user_id'], message = msg) # type: ignore
        
        except:
            await send_to_superusers(bot, f"推送时部分失败了呢") # type: ignore
    
        end = time.perf_counter()

        await session.send(f'已推送到[{f_list}]位用户\n耗时：{round(end - start, 3)}')

# @on_command('send_to_qq', aliases=['对QQ'], only_to_me=False)
# async def send_to_qq(session: CommandSession):
#     if session.event.user_id in master:
#         msg = session.current_arg.strip()
    
#         if not msg:
#             msg = session.get('message', prompt='请告诉吾辈完整内容呢...\n例：对QQ 12345647(QQ号) message')
        
#         lg = msg.split(' ')

#         qq = lg[0]
#         msg = lg[1]

#         try:
#             await bot.send_private_msg(user_id = qq, message = msg) # type: ignore
#         except:
#             await session.send('发送失败，请重试')
        
#         await session.send('推送完成！')