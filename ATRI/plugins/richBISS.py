import re
import json
import nonebot
from datetime import datetime

from ATRI.modules.response import request_api
from ATRI.modules.funcControl import checkNoob


bot = nonebot.get_bot()

def now_time():
    now_ = datetime.now()
    hour = now_.hour
    minute = now_.minute
    now = hour + minute / 60
    return now


BILI_REPORT_FORMAT = """[{aid}] Info:
Title: {title}
bid: {bid}
Viev: {view} Like: {like}
Coin: {coin} Share: {share}
Link:
{aid_link}
{bid_link}"""

table='fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
tr={}
for i in range(58):
	tr[table[i]]=i
s=[11,10,3,8,4,6]
xor=177451812
add=8728348608

def dec(x):
	r=0
	for i in range(6):
		r+=tr[x[s[i]]]*58**i
	return (r-add)^xor

def enc(x):
	x=(x^xor)+add
	r=list('BV1  4 1 7  ')
	for i in range(6):
		r[s[i]]=table[x//58**i%58]
	return ''.join(r)


@bot.on_message("group")
async def Fuck_bili_rich(context):
    user = str(context["user_id"])
    group = context["group_id"]
    if checkNoob(user, group):
        if 0 <= now_time() < 5.5:
            pass
        else:
            msg = str(context["message"])
            pattern = re.compile(r"BV\S+\?")
            bv = re.findall(pattern, msg)
            if bv:
                bv = bv[0]
                bv = bv.replace('?', '')
                print(bv)

                aid = str(dec(bv))
                ad = 'av' + aid
                URL = f'https://api.imjad.cn/bilibili/v2/?aid={aid}'

                try:
                    res = request_api(URL)
                    mg = json.loads(res)
                    msg = BILI_REPORT_FORMAT.format(
                        title = mg["data"]["title"],

                        view = mg["data"]["stat"]["view"],
                        coin = mg["data"]["stat"]["coin"],
                        share = mg["data"]["stat"]["share"],
                        like = mg["data"]["stat"]["like"],

                        bid = mg["data"]["bvid"],
                        bid_link = mg["data"]["short_link"],

                        aid = ad,
                        aid_link = f'https://b23.tv/{ad}'
                        )

                    await bot.send_msg( # type: ignore
                        group_id = group,
                        message = msg
                        )
                except:
                    pass


REPORT_FORMAT = """Status: {status}
Song id: {id}
Br: {br}
Download: {url}
MD5: {md5}"""

@bot.on_message("group")
async def Fuck_CloudMusic(context):
    user = str(context["user_id"])
    group = context["group_id"]
    if checkNoob(user, group):
        if 0 <= now_time() < 5.5:
            pass
        else:
            msg = str(context["message"])
            pattern = re.compile(r"song\S+\/|id=\S+\&")
            music_id = re.findall(pattern, msg)
            if 'music.163.com' in msg:
                if music_id:
                    music_id = str(music_id[0])
                    music_id = re.findall(r"-?[1-9]\d*", music_id)
                    URL = f'https://api.imjad.cn/cloudmusic/?type=song&id={music_id[0]}&br=320000'
                    print(URL)

                    try:
                        res = request_api(URL)
                        mg = json.loads(res)

                        msg = REPORT_FORMAT.format(
                            status = mg["code"],
                            id = mg["data"][0]["id"],
                            br = mg["data"][0]["br"],
                            url = mg["data"][0]["url"],
                            md5 = mg["data"][0]["md5"],
                            )
                        await bot.send_msg(
                            group_id = group,
                            message = msg
                            ) # type: ignore
                    except:
                        pass