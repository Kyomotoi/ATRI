import os
import json
import nonebot
from nonebot import on_command, CommandSession
from pathlib import Path

from nonebot.permission import GROUP_ADMIN

import config


bot = nonebot.get_bot()
master = config.SUPERUSERS


@on_command('switch', aliases = ['on', 'off'], only_to_me = False, permission = GROUP_ADMIN)
async def _(session: CommandSession):
    group = session.event.group_id
    try:
        with open(Path('.') / 'ATRI' / 'data' / 'groupData' / f'{group}' / 'switch.json', 'r') as f:
            data = json.load(f)
    except:
        try:
            os.mkdir(Path('.') / 'ATRI' / 'data' / 'groupData' / f'{group}')
        except:
            pass
        data = {}
        data["pixiv_seach_img"] = "on"
        data["pixiv_seach_author"] = "on"
        data["pixiv_daily_rank"] = "on"
        data["setu"] = "on"
        data["setu_img"] = "on"
        data["anime_search"] = "on"
        data["change_face"] = "on"
        data["chouYou"] = "on"
        data["saucenao_search"] = "on"
        with open(Path('.') / 'ATRI' / 'data' / 'groupData' / f'{group}' / 'switch.json', 'w') as f:
            f.write(json.dumps(data))
            f.close()


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

        elif com == 'Setu':
            data["setu"] = "on"
        
        elif com == 'SetuIMG':
            data["setu_img"] = "on"
        
        elif com == "AnimeSearch":
            data["anime_search"] = "on"
        
        elif com == 'AIchFace':
            data["change_face"] = "on"
        
        elif com == 'Kyaru':
            data["chouYou"] = "on"
        
        elif com == 'SauceNAO':
            data["saucenao_search"] = "on"
        
        else:
            session.finish('未找到此功能...请检查拼写奥...')

    elif switch == 'off':
        if com == 'PixivSearchIMG':
            data["pixiv_seach_img"] = "off"
        
        elif com == 'PixivSearchAuthor':
            data["pixiv_seach_author"] = "off"
        
        elif com == 'PixivRank':
            data["pixiv_daily_rank"] = "off"

        elif com == 'Setu':
            data["setu"] = "off"
        
        elif com == 'SetuIMG':
            data["setu_img"] = "off"
        
        elif com == "AnimeSearch":
            data["anime_search"] = "off"
        
        elif com == 'AIchFace':
            data["change_face"] = "off"
        
        elif com == 'Kyaru':
            data["chouYou"] = "off"
        
        elif com == 'SauceNAO':
            data["saucenao_search"] = "off"
        
        else:
            session.finish('未找到此功能...请检查拼写奥...')
    
    f2 = open(Path('.') / 'ATRI' / 'data' / 'groupData' / f'{group}' / 'switch.json', 'w')
    f2.write(json.dumps(data))
    f2.close()

    await session.send('Success！')


@on_command('allSwitch', aliases = ['allon', 'alloff'], only_to_me = False)
async def _(session: CommandSession):
    if session.event.user_id in master:
        with open(Path('.') / 'ATRI' / 'modules' / 'funcControl' / 'ALLswitch.json', 'r') as f:
            data = json.load(f)
        
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

            elif com == 'Setu':
                data["setu"] = "on"
            
            elif com == 'SetuIMG':
                data["setu_img"] = "on"
            
            elif com == "AnimeSearch":
                data["anime_search"] = "on"
            
            elif com == 'AIchFace':
                data["change_face"] = "on"
            
            elif com == 'Kyaru':
                data["chouYou"] = "on"
            
            elif com == 'SauceNAO':
                data["saucenao_search"] = "on"
            
            else:
                session.finish('未找到此功能...请检查拼写奥...')

        elif switch == 'off':
            if com == 'PixivSearchIMG':
                data["pixiv_seach_img"] = "off"
            
            elif com == 'PixivSearchAuthor':
                data["pixiv_seach_author"] = "off"
            
            elif com == 'PixivRank':
                data["pixiv_daily_rank"] = "off"

            elif com == 'Setu':
                data["setu"] = "off"
            
            elif com == 'SetuIMG':
                data["setu_img"] = "off"
            
            elif com == "AnimeSearch":
                data["anime_search"] = "off"
            
            elif com == 'AIchFace':
                data["change_face"] = "off"
            
            elif com == 'Kyaru':
                data["chouYou"] = "off"
            
            elif com == 'SauceNAO':
                data["saucenao_search"] = "off"
            
            else:
                session.finish('未找到此功能...请检查拼写奥...')
        
        f2 = open(Path('.') / 'ATRI' / 'modules' / 'funcControl' / 'ALLswitch.json', 'w')
        f2.write(json.dumps(data))
        f2.close()

        await session.send('Success！')