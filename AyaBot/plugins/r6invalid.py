import json
import requests
from nonebot import on_command, CommandSession


API_URL = 'https://r6.apitab.com/search/'


LIST = """{player} 情况如下:
Level:{level}
HeadShot(%):{generalpvp_hsrate}
Ranked:
    KD:{rankedpvp_kd}
    WP:{rankedpvp_wl}
Casual:
    KD:{casualpvp_kd}
    WP:{casualpvp_wl}
Ban for:
    Attacker:{attacker}
    Defender:{defender}"""


@on_command('r6', aliases=['r6查询', 'r6战绩查询', 'r6战绩', 'R6战绩', 'R6战绩查询', 'R6查询 '], only_to_me=False)
async def _(session: CommandSession):
    player = session.get('player', prompt='请发送需要查询的ID')
    try:
        res = API_URL + player
        res1 = requests.get(res)
        res1.encoding = 'utf-8'
        html = res1.text
        r6 = json.loads(html)
        await session.send(LIST.format(
            player=r6["player"]["p_name"],
            level=r6["stats"]["level"],
            generalpvp_hsrate=r6["stats"]["generalpvp_hsrate"],
            rankedpvp_kd=r6["stats"]["rankedpvp_kd"],
            rankedpvp_wl=r6["stats"]["rankedpvp_wl"],
            casualpvp_kd=r6["stats"]["casualpvp_kd"],
            casualpvp_wl=r6["stats"]["casualpvp_wl"],
            attacker=r6["op_main"]["attacker"],
            defender=r6["op_main"]["defender"],
            )
        )
    except:
        await session.send('获取数据时出问题，请重试')
        return