import json
import nonebot
from nonebot import on_command, CommandSession


bot = nonebot.get_bot()
master = bot.config.SUPERUSERS


@on_command('switch', aliases = ['on', 'off'], only_to_me = False)
async def _(session: CommandSession):
    with open("ATRI/plugins/switch/switch.json", 'r') as f:
        data = json.load(f)
    print(data)

    if session.event.user_id in master:
        command = session.event.raw_message.split(' ', 1)
        switch = command[0]
        com = command[1]
        print(command)

        if switch == 'on':
            if com == 'PixivSearchIMG':
                data["pixiv_seach_img"] = "on"
            
            elif com == 'PixivSearchAuthor':
                data["pixiv_seach_author"] = "on"
            
            elif com == 'PixivRank':
                data["pixiv_daily_rank"] = "on"
            
            elif com == 'FriendADD':
                data["approve_friend_add"] = "on"
            
            elif com == 'GroupInvite':
                data["approve_invite_join_group"] = "on"

            elif com == 'Setu':
                data["setu"] = "on"
            
            elif com == 'SetuIMG':
                data["setu_img"] = "on"
            
            elif com == 'Hbook':
                data["hbook"] = "on"
            
            elif com == 'AIchFace':
                data["change_face"] = "on"
            
            elif com == 'Kyaru':
                data["chouYou"] = "on"

            else:
                pass

        elif switch == 'off':
            if com == 'PixivSearchIMG':
                data["pixiv_seach_img"] = "off"
            
            elif com == 'PixivSearchAuthor':
                data["pixiv_seach_author"] = "off"
            
            elif com == 'PixivRank':
                data["pixiv_daily_rank"] = "off"

            elif com == 'FriendADD':
                data["approve_friend_add"] = "off"
            
            elif com == 'GroupInvite':
                data["approve_invite_join_group"] = "off"

            elif com == 'Setu':
                data["setu"] = "off"
            
            elif com == 'SetuIMG':
                data["setu_img"] = "off"
            
            elif com == 'Hbook':
                data["hbook"] = "off"
            
            elif com == 'AIchFace':
                data["change_face"] = "off"
            
            elif com == 'Kyaru':
                data["chouYou"] = "off"
            
            else:
                pass
        
        f2 = open("ATRI/plugins/switch/switch.json", 'w')
        f2.write(json.dumps(data))
        f2.close()

        await session.send('Success！')
    
    else:
        await session.send('恁哪位？')