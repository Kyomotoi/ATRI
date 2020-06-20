# -*- coding:utf-8 -*-
import re
import json
import demjson
import requests
from os import path
from pprint import pformat, pprint
from urllib.parse import urlencode
from nonebot import on_command, CommandSession
from AyaBot.plugins.module import google_translate


# 国外版 数据更新非常及时
# 必须挂木弟子
# 成功把之前的屎优化了！OHHHHHHHHHHHH
# 如需使用国内版，请查看下面的链接，下载后与这个文件替换
# https://github.com/Kyomotoi/covid19/tree/master/Domestic



url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/total"


LIST = """截至: {lastChecked}
国家: {location}
已治愈: {recovered}
已经死亡: {deaths}
总感染数: {confirmed}
现存感染人数: {nowConfirmed}
最后检查时间: {lastReported}"""


@on_command('covid19', aliases=['疫情', '疫情查询', '疫情情况'], only_to_me=False)
async def covid19(session: CommandSession):
    country = session.get('country', prompt='请键入需要查询的国家(例:中国)')
    if country == '美国':
        pass
    else:
        re_msg = google_translate.translate(country[:4999], to='en', source='zh-CN')
    # if re_msg[0]!='':
    #     await session.send(re_msg[0])
    await session.send('开始搜寻...\n如返回Global则为国家名有问题')
    try:
        querystring = {"country":"cy"}
        if country == '美国':
            re_msg = 'US'
            querystring["country"] = re_msg
        else:
            querystring["country"] = re_msg[0]
        print(querystring)
        headers = {
            'x-rapidapi-host': "covid-19-coronavirus-statistics.p.rapidapi.com",
            'x-rapidapi-key': "a852be0d03msh8bd4299fe71bfeep100861jsn185ea925449c"
            }
        response = requests.request("GET", url, headers=headers, params=querystring)
        # print(response.text)
        html = response.text
        c19 = json.loads(html)
        await session.send(LIST.format(
            lastChecked=c19["data"]["lastReported"],
            location=c19["data"]["location"],
            recovered=c19["data"]["recovered"],
            deaths=c19["data"]["deaths"],
            confirmed=c19["data"]["confirmed"],
            nowConfirmed=c19["data"]["confirmed"] - c19["data"]["deaths"] - c19["data"]["recovered"],
            lastReported=c19["data"]["lastChecked"],
            )
        )
    except:
        await session.send('搜索出问题了呢，重新试试?')

@covid19.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        if stripped_arg:
            session.state['country'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('要查询的国家不能为空，请重新输入')
    session.state[session.current_key] = stripped_arg
