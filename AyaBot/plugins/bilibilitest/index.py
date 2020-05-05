import math
import re
import requests
from typing import Optional, List, Any, Dict
from nonebot import CommandSession, CommandGroup
from aiocache import cached

from datetime import datetime
import pytz
from pandas import Timestamp

# from .aio import *

#get TIME
CST = 'Asia/Shanghai'

def beijing_time_now(freq: Optional[str] = None) -> datetime:
    now = datetime.now(pytz.timezone(CST))
    if freq is not None:
        now = Timestamp(now).round(freq)
    return now


def beijing_from_timestamp(timestamp: int) -> datetime:
    return datetime.fromtimestamp(timestamp, pytz.timezone(CST))



cg = CommandGroup('bilibili_anime')

API_URL = 'https://bangumi.bilibili.com/media/web_api/search/result?season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month={month}&pub_date={year}&style_id=-1&order=3&st=1&sort=0&page=1&season_type=1&pagesize=20'
WEB_URL = 'https://www.bilibili.com/anime/index/#season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month={month}&pub_date={year}&style_id=-1&order=3&st=1&sort=0&page=1'


@cached(ttl= 5 * 60)
async def get_anime_list(year: int, month: int) -> Optional[List[Dict[str, Any]]]:
    api_url = API_URL.format(year=year, month=month)
    res = await requests.get(api_url)
    payload = await res.json()
    
    if not payload or payload.get('code') != 0:
        return None
    
    return payload['result']['data']


@cg.command('fan', aliases=['新番', '番剧索引', '番剧'], only_to_me=False)
async def fan(session: CommandSession):
    now = beijing_time_now()
    year = session.state.get('year', now.year)
    month = session.state.get('month', now.month)
    month = math.ceil(month / 3) * 3 - 3 + 1

    anime_list = await get_anime_list(year, month)
    if not anime_list:
        session.finish('并没有找到相关的番剧...再试一次..?')
    
    reply = f'{year}/{month}番剧\n按照热度进行排序,前20部如下: \n'
    for anime in anime_list:
        title = anime.get('title')
        index_show = anime.get('index_show', 'Error')
        if not title:
            continue
        reply += f'{title}  {index_show}\n'
    
    web_url = WEB_URL.format(year=year, month=month)
    reply += f'\n详细请见官网 {web_url}'
    session.finish(reply)


@fan.args_parser
async def _(session: CommandSession):
    arg = session.current_arg_text.split()

    year = None
    month = None
    if len(arg) == 2 and re.fullmatch(r'(?:20)?\d{2}', arg[0]) and re.fullmatch(r'\d{1,2}', arg[1]):
        year = int(arg[0]) if len(arg[0]) > 2 else 2000 + int (arg[0])
        month = int(arg[1])
    elif len(arg) == 1 and re.fullmatch(r'\d{1,2}', arg[0]):
        month = int(arg[0])
    elif len(arg) == 1 and re.fullmatch(r'(?:20)?\d{2}-\d{1,2}', arg[0]):
        year, month = [int(x) for x in arg[0].split('-')]
        year = 2000 + year if year < 1000 else year
    elif len(arg):
        await session.send('脑子变奇怪了...无法识别master的信息,先给份本季的番8...')

    if year is not None:
        session.state['year'] = year
    if month is not None:
        session.state['month'] = month