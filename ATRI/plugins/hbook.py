import re
import time
import json
from pathlib import Path
from datetime import datetime
from random import choice
from nonebot import on_command, CommandSession

from ATRI.modules import response # type: ignore


def now_time():
    now_ = datetime.now()
    hour = now_.hour
    minute = now_.minute
    now = hour + minute / 60
    return now


pattern = r"来(.*?)[点丶份张幅](.*?)的?本子"

@on_command('hbook', patterns = pattern, only_to_me = False)
async def _(session: CommandSession):
    h_user = session.event.user_id
    group = session.event.group_id
    try:
        with open(Path('.') / 'ATRI' / 'plugins' / 'noobList' / 'noobGroup.json', 'r') as f:
            data = json.load(f)
    except:
        data = {}
    try:
        with open(Path('.') / 'ATRI' / 'plugins' / 'noobList' / 'noobList.json', 'r') as f:
            data1 = json.load(f)
    except:
        data1 = {}

    if str(group) in data.keys():
        pass
    else:
        if str(h_user) in data1.keys():
            pass
        else:
            if 0 <= now_time() < 5.5:
                await session.send(
                    choice(
                        [
                            'zzzz......',
                            'zzzzzzzz......',
                            'zzz...好涩哦..zzz....',
                            '别...不要..zzz..那..zzz..',
                            '嘻嘻..zzz..呐~..zzzz..'
                        ]
                    )
                )
            else:
                with open(Path('.') / 'ATRI' / 'plugins' / 'switch' / 'switch.json', 'r') as f:
                    data = json.load(f)
                
                if data["hbook"] == "on":
                    num = 1
                    tag = ''
                    start = time.perf_counter()
                    h_msg = str(session.event.message)

                    info = re.findall(pattern, h_msg)
                    if info:
                        num = int(info[0][0] or 1)
                        tag = str(info[0][1])
                    if num > 5:
                        await session.send('你是不是涩批啊！要那么多干啥？！我最多发5份！')
                        num = 5
                    
                    h_type = session.event.detail_type

                    try:
                        header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
                        keyword = {'show':'title,titleen,tags','keyboard':tag}
                        print(keyword)

                        res = await response.post_bytes('https://b-upp.com/search/', headers=header, data=keyword)
                        res = res.decode()
                    except:
                        session.finish('貌似请求数据失败了...')

                    if '没有搜索到相关的内容' in res:
                        n_msg = '...似乎没有找到[{}]相关的本子呢'.format(tag)
                        await session.send(message=n_msg)
                    
                    else:
                        p = '<a href="(.*?)" target="_blank" title="(.*?)">'
                        data = re.findall(p,res)
                        n = len(data)
                        limit = num
                        
                        if n > limit: # type: ignore
                            n = limit # type: ignore

                        msg = f'据提供信息，已查询到{n}本关键词为[{tag}]的本子:'
                        if h_type == 'group':
                            msg = f'[CQ:at,qq={h_user}]\n根据提供信息，已查询到{n}本关键词为[{tag}]的本子:'
                        for i in range(n):
                            msg0 = ('\n——————————\n本子链接：https://b-upp.com%s \n本子标题：%s '%(data[i]))
                            msg += msg0
                        end = time.perf_counter()
                        msg0 = f'\n——————————\n耗时: {round(end - start, 3)}s'
                        msg += msg0

                        await session.send(msg)

                else:
                    await session.send('该功能已禁用...')