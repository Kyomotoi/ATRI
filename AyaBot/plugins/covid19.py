import json
import requests
from nonebot import on_command, CommandSession


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
    country = session.get('country', prompt='请用Eng键入需要查询的国家(例:China)')
    await session.send('开始搜寻...\n如返回国名为Global的则为提供的国家名有问题，必须为英文全称')
    try:
        querystring = {"country":"cy"}
        querystring["country"] = country
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
            lastChecked=c19["data"]["lastChecked"],
            location=c19["data"]["location"],
            recovered=c19["data"]["recovered"],
            deaths=c19["data"]["deaths"],
            confirmed=c19["data"]["confirmed"],
            nowConfirmed=c19["data"]["confirmed"] - c19["data"]["deaths"] - c19["data"]["recovered"],
            lastReported=c19["data"]["lastReported"],
            )
        )
    except:
        await session.send('搜索出问题了呢，重新试试?')