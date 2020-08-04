# -*- coding:utf-8 -*-
import re
import time
import json
from nonebot import on_command, CommandSession

from ATRI.modules import response # type: ignore


@on_command('hbook', aliases = ['本子', '本子搜索', '本子查询'], only_to_me = False)
async def _(session: CommandSession):
    with open('ATRI/plugins/switch/switch.json', 'r') as f:
        data = json.load(f)
    
    if data["hbook"] == 0:
        start = time.perf_counter()
        h_msg = session.current_arg.strip()

        if not h_msg:
            h_msg = session.get('message', prompt='要冲了吗？速发关键词')
        
        h_type = session.event.detail_type
        h_user = session.event.user_id

        header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
        keyword = {'show':'title,titleen,tags','keyboard':h_msg}

        res = await response.post_bytes('https://b-upp.com/search/', headers=header, data=keyword)
        res = res.decode()

        if '没有搜索到相关的内容' in res:
            n_msg = '...似乎没有找到[{}]相关的本子呢'.format(h_msg)
            await session.send(message=n_msg)
        
        else:
            p = '<a href="(.*?)" target="_blank" title="(.*?)">'
            data = re.findall(p,res)
            n = len(data)

            if h_type == 'group':
                limit = 3

            elif h_type == 'private':
                limit = 10
            
            if n > limit: # type: ignore
                n = limit # type: ignore

            msg = f'根据提供信息，已查询到{n}本关键词为[{h_msg}]的本子:'
            if h_type == 'group':
                msg = f'[CQ:at,qq={h_user}]\n根据提供信息，已查询到{n}本关键词为[{h_msg}]的本子:'
            for i in range(n):
                msg0 = ('\n——————————\n本子链接：https://b-upp.com%s \n本子标题：%s '%(data[i]))
                msg += msg0
            end = time.perf_counter()
            msg0 = f'\n——————————\n耗时: {round(end - start, 3)}s'
            msg += msg0

            await session.send(message=msg)

    else:
        await session.send('该功能已禁用...')