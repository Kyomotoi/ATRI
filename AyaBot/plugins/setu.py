import re
import json
import random
import urllib
import nonebot
import requests
from aiohttp import ClientSession
from nonebot import on_command, CommandSession


async def post_bytes(url, headers=None,data=None):
    async with ClientSession() as asyncsession:
        async with asyncsession.post(url,headers=headers,data=data) as response:
            b = await response.read()
    return b


a = '1'
b = '2'
c = '3'

hphoto_switch = True
hbook_switch = True
@on_command('hphoto_switch', aliases=['开启', '关闭'], only_to_me=False)
async def _(session: CommandSession):
    if session.ctx['user_id'] in session.bot.config.SUPERUSERS:
        command = session.ctx['raw_message'].split(' ', 1)
        switch = command[0]
        com = command[1]
        global hphoto_switch
        if switch == '开启':
            if com == '涩图':
                hphoto_switch = True
            elif com == '本子':
                hbook_switch = True
            else:
                pass
        elif switch == '关闭':
            if com == '涩图':
                hphoto_switch = False
            elif com == '本子':
                hbook_switch = False
            else:
                pass
        await session.send('完成')
    else:
        await session.send('恁哪位?')
            

@on_command('hphoto', aliases=['涩图', '涩图来！', '涩图来', '图来', '开冲', '来点好康的', '来丶好康的', '车来'], only_to_me=False)
async def _(session: CommandSession):
    if hphoto_switch:
        r = random.choice([a, b])
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
            url = 'https://api.lolicon.app/setu/'
            values = {
                "apikey": "574300555ee56eb2be5e03",
                "r18": "0",
                "num": "1"
             }
            response = requests.get(url, params=values)
            html = response.text
            se = json.loads(html)
            # print(se)
            title=se["data"][0]["title"]
            pid=se["data"][0]["pid"]
            setu=se["data"][0]["url"]
            await session.send(f'Title: {title}\nPid: {pid}\n[CQ:image,file={setu}]')
        # if r == '2':
        #     URL = 'https://danbooru.donmai.us/post.json'
        #     values = {
        #         "api_key": "UoTNRNeta73tqqdGVvsU9mmH"
        #     }
        #     response = requests.get(URL, params=values)
        #     html = response.text
        #     hp = json.loads(html)
        #     re = random.randint(0,19)
        #     pt = hp[re]["file_url"]
        #     await session.send(f'[CQ:image,file={pt}]')
        # if r == '3':
        #     URL = 'https://yande.re/post.json'
        #     values = {
        #         "api_key": "zgBbal8sZVuRYp3UNX5Frg"
        #     }
        #     response = requests.get(URL, params=values)
        #     html = response.text
        #     hp = json.loads(html)
        #     re = random.randint(0,39)
        #     pt = hp[re]["jpeg_url"]
        #     await session.send(f'[CQ:image,file={pt}]')


@on_command('hbook', aliases=['本子', '找本子', '本子查询'], only_to_me=False)
async def _(session: CommandSession):
    if hbook_switch:
        h_msg = session.current_arg.strip()
        if not h_msg:
            h_msg = session.get('message', prompt='要冲了吗？速发关键词')
        h_type = session.ctx['message_type']
        h_qq = session.ctx['user_id']
        header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
        keyword = {'show':'title,titleen,tags','keyboard':h_msg}
        responce = await post_bytes('https://b-upp.com/search/', headers=header, data=keyword)
        responce = responce.decode()
        if '没有搜索到相关的内容' in responce:
            n_msg = '...似乎没有找到[{}]相关的本子呢'.format(h_msg)
            await session.send(message=n_msg)
        else:
            p = '<a href="(.*?)" target="_blank" title="(.*?)">'
            data = re.findall(p,responce)
            n = len(data)
            if h_type == 'group':
                limit = 3
            elif h_type == 'private':
                limit = 10
            if n > limit:
                n = limit
            msg = f'根据提供信息，已查询到{n}本关键词为[{h_msg}]的本子:'
            if h_type == 'group':
                msg = f'[CQ:at,qq={h_qq}]\n根据提供信息，已查询到{n}本关键词为[{h_msg}]的本子:'
            for i in range(n):
                msg0 = ('\n——————————\n本子链接：https://b-upp.com%s \n本子标题：%s '%(data[i]))
                msg += msg0
            await session.send(message=msg)