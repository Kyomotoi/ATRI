import json
import requests
import pandas as pd
from nonebot import on_command, CommandSession
from datetime import datetime


url_1 = 'https://api.imjad.cn/hitokoto/?cat=a&charset=utf-8&length=50&encode=json&fun=sync&source='
response_1 = requests.get(url=url_1).json()
data_1 = json.load(response_1)

filename1 = "data_1.json"

LIST = """一言
{hitokoto}
by {source}
"""

@on_command('hitokoto', aliases=['一言'], only_to_me=False)
async def _(session: CommandSession):
    f = open(filename1, encoding='utf-8')
    setting = json.load(f)
    await session.send(LIST.format(
        hitokoto=setting["hitokoto"],
        source=setting["source"]
        )
    )


#开发ing