import requests
import json
from nonebot import on_command, CommandSession


@on_command('番剧索引')
async def _(session: CommandSession):
    # url = 'https://api.bilibili.com/pgc/season/index/result?season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&year=-1&style_id=-1&order=3&st=1&sort=0&page=1&season_type=1&pagesize=20&type=1'
    
    res = requests.get(
        'https://api.bilibili.com/pgc/season/index/result?season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&year=-1&style_id=-1&order=3&st=1&sort=0&page=1&season_type=1&pagesize=20&type=1',
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }
    )

    data = res.json()
    print(['list'])
    # JSON.data.list = data['JSON.data.list']
    # reply = ''
    # for JSON.data.list in JSON.data.list:
    #     title = data.list['title']
    #     url = data.list['link']
    #     reply += f'\n{title}\n{url}'
    # session.send('今日番剧索引如下: \n' + reply)

    # if not list:
    #     await session.send('暂时无法返回请求，或服务器变奇怪了...')
    #     return