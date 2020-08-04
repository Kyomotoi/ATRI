# -*- coding:utf-8 -*-
import json
import nonebot
from nonebot import on_command, CommandSession


bot = nonebot.get_bot()
master = bot.config.SUPERUSERS


@on_command('switch', aliases = ['开启', '关闭'], only_to_me = False)
async def _(session: CommandSession):
    with open(f"ATRI/plugins/switch/switch.json", 'r') as f:
        data = json.load(f)

    if session.event.user_id in master:
        command = session.event.raw_message.split(' ', 1)
        switch = command[0]
        com = command[1]

        if switch == '开启':
            if com == 'p站搜图':
                data["pixiv_seach_img"] = 0
            
            elif com == '画师':
                data["pixiv_seach_author"] = 0
            
            elif com == 'P站排行榜':
                data["pixiv_daily_rank"] = 0
            
            elif com == '好友添加':
                data["approve_friend_add"] = 0
            
            elif com == '群邀请':
                data["approve_invite_join_group"] = 0

            elif com == '涩图':
                data["setu"] = 0
            
            elif com == '本子':
                data["hbook"] = 0
            
            else:
                pass

        elif switch == '关闭':
            if com == 'p站搜图':
                data["pixiv_seach_img"] = 1
            
            elif com == '画师':
                data["pixiv_seach_author"] = 1
            
            elif com == 'P站排行榜':
                data["pixiv_daily_rank"] = 1

            elif com == '好友添加':
                data["approve_friend_add"] = 1
            
            elif com == '群邀请':
                data["approve_invite_join_group"] = 1

            elif com == '涩图':
                data["setu"] = 1
            
            elif com == '本子':
                data["hbook"] = 1
            
            else:
                pass
        
        a = json.dumps(data)
        f2 = open(f"ATRI/plugins/switch/switch.json", 'w')
        f2.write(a)
        f2.close

        await session.send('设置完成！')
    
    else:
        await session.send('恁哪位？')