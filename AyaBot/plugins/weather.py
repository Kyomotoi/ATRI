import json
import requests
from nonebot import on_command, CommandSession


API_URL = 'https://www.tianqiapi.com/free/day?appid=36628957&appsecret=WKn4dtVg&city='


LIST = """{city} 今日信息如下:
更新时间:{time}
天气情况:{wea}
空气质量:{air}
温度:
    现在温度:{tem}
    最高温度:{temday}
    最低温度:{temnight}
风向:{win}
风力等级:{winspeed}
风速:{winmeter}"""


@on_command('weather', aliases=['天气', '查天气', '天气查询'], only_to_me=False)
async def weather(session: CommandSession):
    city = session.get('city', prompt='你想查哪个城市呢？')
    try:
        res = API_URL + city
        res1 = requests.get(res)
        res1.encoding = 'utf-8'
        html = res1.text
        wt = json.loads(html)
        await session.send(LIST.format(
            city=wt["city"],
            time=wt["update_time"],
            wea=wt["wea"],
            tem=wt["tem"],
            temday=wt["tem_day"],
            temnight=wt["tem_night"],
            win=wt["win"],
            winspeed=wt["win_speed"],
            winmeter=wt["win_meter"],
            air=wt["air"]
            )
        )
    except:
        await session.send('获取数据时出问题，请重试')
        return