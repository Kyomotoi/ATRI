import json
import random
import nonebot
import requests
from nonebot import on_command, CommandSession

a = '1'
b = '2'
c = '3'

hphoto_switch = True
@on_command('hphoto_switch', aliases=['开启一图', '关闭一图'], only_to_me=False)
async def _(session: CommandSession):
    if session.ctx['user_id'] in session.bot.config.SUPERUSERS:
        command = session.ctx['raw_message'].split(' ', 1)
        switch = command[0]
        global hphoto_switch
        if switch == '开启涩图':
            hphoto_switch = True
        if switch == '关闭涩图':
            hphoto_switch = False
        await session.send('完成')
    else:
        await session.send('恁哪位?')
            

@on_command('hphoto', aliases=['一图'], only_to_me=False)
async def _(session: CommandSession):
    if hphoto_switch:
        r = random.choice([a, b, c])
        print(r)
        if r == '1':
            URL = 'https://konachan.com/post.json'
            response = requests.request("GET", URL)
            html = response.text
            hp = json.loads(html)
            re = random.randint(0,20)
            pt = hp[re]["jpeg_url"]
            await session.send(f'[CQ:image,file={pt}]')
        if r == '2':
            URL = 'https://danbooru.donmai.us/posts.json'
            response = requests.request("GET", URL)
            html = response.text
            hp = json.loads(html)
            re = random.randint(0,19)
            pt = hp[re]["file_url"]
            await session.send(f'[CQ:image,file={pt}]')
        if r == '3':
            URL = 'https://yande.re/post.json'
            response = requests.request("GET", URL)
            html = response.text
            hp = json.loads(html)
            re = random.randint(0,39)
            pt = hp[re]["jpeg_url"]
            await session.send(f'[CQ:image,file={pt}]')
        
