import json
import nonebot
from orjson import loads
from html import unescape


import requests

def request_api(url):
    response = requests.request("GET", url)
    html = response.text
    return html



REPORT_FORMAT = """({aid})信息如下:
Title: {title}
aid: {aid}
bid: {bid}
观看: {view} 点赞: {like}
投币: {coin} 转发: {share}
观看链接:
{aid_link}
{bid_link}
{img}"""


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


@nonebot.on_natural_language(only_to_me = False)
async def fk_tx_app_bilibili(session: nonebot.NLPSession):
    rich_message = [x for x in session.ctx['message'] if x.get('type') == 'rich']

    if not rich_message:
        return

    rich_message = rich_message[0]['data']

    if '小程序' or '哔哩哔哩' not in rich_message['title']:
        return
    
    rich_message = rich_message['content']
    data = loads(unescape(rich_message))
    
    if 'detail_1' not in str(rich_message):
        return
    
    URL = data['detail_1']['qqdocurl']
    rep = URL.replace('?', '/')
    rep = rep.split('/')
    biv = rep[4]

    aid = str(dec(biv))

    url = f'https://api.imjad.cn/bilibili/v2/?aid={aid}'
    ad = 'av' + aid
    print(ad)

    dc = json.loads(request_api(url))

    pic = dc["data"]["pic"]

    await session.send(REPORT_FORMAT.format(
        title = dc["data"]["title"],

        view = dc["data"]["stat"]["view"],
        coin = dc["data"]["stat"]["coin"],
        share = dc["data"]["stat"]["share"],
        like = dc["data"]["stat"]["like"],

        bid = biv,
        bid_link = dc["data"]["short_link"],

        aid = ad,
        aid_link = f'https://b23.tv/{ad}',

        img = f'[CQ:image,file={pic}]',
        )
    )
