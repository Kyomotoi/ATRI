import time
import json
from datetime import datetime
from random import choice
import nonebot
from nonebot import on_command, CommandSession

import config
from ATRI.modules.response import request_api
from ATRI.modules.error import errorBack
from ATRI.modules.funcControl import checkSwitch, checkNoob


bot = nonebot.get_bot()
master = config.SUPERUSERS
__plugin_name__ = "pixiv"
__plugin_name1__ = "pixiv_seach_img"
__plugin_name2__ = "pixiv_seach_author"
__plugin_name3__ = "pixiv_daily_rank"

URL_1 = 'https://api.imjad.cn/pixiv/v1/?type=illust&id=' #单图搜索
URL_2 = 'https://api.imjad.cn/pixiv/v1/?type=member_illust&id=' #画师作品搜索
URL_3 = 'https://api.imjad.cn/pixiv/v1/?type=rank' #每日排行榜


IMG_SEACH_REPLY = """[CQ:at,qq={user}]
搜索结果如下:
Pid: {pid}
Title: {title}
宽高: {width}x{height}
Tags: {tags}
账号名称: {account}
名称: {name}
Link: {user_link}
{img}
---------------
完成时间:{time}s"""


def now_time():
    now_ = datetime.now()
    hour = now_.hour
    minute = now_.minute
    now = hour + minute / 60
    return now


@on_command('pixiv_seach_img', aliases = ['p站搜图', 'P站搜图', '批站搜图'], only_to_me = False)
async def _(session: CommandSession):
    user = session.event.user_id
    group = session.event.group_id
    if checkNoob(user, group):
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
            if checkSwitch(__plugin_name1__, group):
                pid = session.current_arg.strip()

                if not pid:
                    pid = session.get('message', prompt = '请告诉ATRI需要查询的Pid码')
                
                start =time.perf_counter()
                await session.send('开始P站搜图')

                URL = URL_1 + pid

                try:
                    dc = json.loads(request_api(URL))
                except:
                    session.finish(errorBack('请求数据失败'))

                img = f'https://pixiv.cat/{pid}.jpg'
                

                end = time.perf_counter()

                try:
                    await session.send(
                        IMG_SEACH_REPLY.format(
                            user = user,
                            pid = pid,
                            title = dc["response"][0]["title"],
                            width = dc["response"][0]["width"],
                            height = dc["response"][0]["height"],
                            tags = dc["response"][0]["tags"],
                            account = dc["response"][0]["user"]["account"],
                            name = dc["response"][0]["user"]["name"],
                            user_link = f'https://www.pixiv.net/users/' + f'{dc["response"][0]["user"]["id"]}',
                            img = img,
                            time = round(end - start, 3)
                        )
                    )
                except:
                    session.finish(errorBack('处理数据失败'))
            
            else:
                await session.send('该功能已关闭...')


@on_command('pixiv_seach_author', aliases = ['画师', '搜索画师', '画师搜索'], only_to_me = False)
async def _(session: CommandSession):
    user = session.event.user_id
    group = session.event.group_id
    if checkNoob(user, group):
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
            if checkSwitch(__plugin_name2__, group):
                author_id = session.current_arg.strip()

                if not author_id:
                    author_id = session.get('message', prompt = '请告诉ATRI需要查询的画师ID')
                
                start =time.perf_counter()
                await session.send(f'开始获取画师{author_id}的前三项作品\n如获取时间过长或许为图片过大上传较慢')

                URL = URL_2 + author_id

                try:
                    dc = json.loads(request_api(URL))
                except:
                    session.finish(errorBack('请求数据失败'))

                d ={}

                try:
                    for i in range(0,3):
                        pid = dc["response"][i]["id"]
                        pidURL = f'https://pixiv.cat/{pid}.jpg'
                        d[i] = [f'{pid}',f'{pidURL}']
                except:
                    session.finish(errorBack('处理数据失败'))
                
                msg0 = (f'[CQ:at,qq={user}]\n画师id:{author_id}，接下来展示前三作品')

                result = sorted(
                            d.items(),
                            key = lambda x:x[1],
                            reverse = True
                )

                t = 0

                for i in result:
                    t += 1
                    msg = (f'\n---------------\n({t})\nPid: {i[1][0]}\n{i[1][1]}')
                    msg0 += msg
                end = time.perf_counter()

                msg1 = (f'\n---------------\n完成时间:{round(end - start, 3)}s')
                msg0 += msg1
                
                await session.send(msg0)
            
            else:
                await session.send('该功能已关闭...')


@on_command('pixiv_daily_rank', aliases = ['P站排行榜', '批站排行榜', 'p站排行榜'], only_to_me = False)
async def _(session: CommandSession):
    user = session.event.user_id
    group = session.event.group_id
    if checkNoob(user, group):
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
            if checkSwitch(__plugin_name__, group):
                await session.send('ATRI正在获取P站每日排行榜前五作品...')

                start =time.perf_counter()

                try:
                    dc = json.loads(request_api(URL_3))
                except:
                    session.finish(errorBack('请求数据失败'))

                d = {}

                try:
                    for i in range(0,5):
                        pid = dc["response"][0]["works"][i]["work"]["id"]
                        pidURL = f'https://pixiv.cat/{pid}.jpg'
                        d[i] = [f'{pid}',f'{pidURL}']
                except:
                    session.finish('处理数据失败')

                msg0 = (f'[CQ:at,qq={user}]')

                result = sorted(
                    d.items(),
                    key = lambda x:x[1],
                    reverse = True
                )

                t = 0

                for i in result:
                    t += 1
                    msg = (f'\n---------------\n({t})\nPid: {i[1][0]}\n{i[1][1]}')
                    msg0 += msg
                end = time.perf_counter()

                msg1 = (f'\n---------------\n完成时间:{round(end - start, 3)}s')
                msg0 += msg1

                await session.send(msg0)
            
            else:
                await session.send('该功能已关闭...')