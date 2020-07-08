import json
import requests
from nonebot import on_command, CommandSession


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


@on_command('bilibili_search_vd', aliases=['b站视频搜索', '批站视频搜索', 'B站视频搜索'], only_to_me=False)
async def bilibili_search_vd(session: CommandSession):

	bi = session.current_arg.strip()
	if not bi:
		bi = session.get('bi', prompt='请输入bv号或av号')

	str_av = 'av'
	str_bv = 'BV'

	if str_av in bi:
		aid = bi
	elif str_bv in bi:
		aid = str(dec(bi))
		print(aid)
	else:
		await session.finish('检查下bv/av号是否输入错误呢...')
	
	URL = f'https://api.imjad.cn/bilibili/v2/?aid={aid}'
	print(URL)

	ad = 'av' + aid
	print(ad)

	try:
		response = requests.request("GET", URL)
	
		try:
			html = response.text
			mg = json.loads(html)
			print('az')

			pic = mg["data"]["pic"]

			await session.send(REPORT_FORMAT.format(
					title = mg["data"]["title"],

					view = mg["data"]["stat"]["view"],
					coin = mg["data"]["stat"]["coin"],
					share = mg["data"]["stat"]["share"],
					like = mg["data"]["stat"]["like"],

					bid = mg["data"]["bvid"],
					bid_link = mg["data"]["short_link"],

					aid = ad,
					aid_link = f'https://b23.tv/{ad}',

					img = f'[CQ:image,file={pic}]',
				)
			)
		
		except:
			await session.send('吾辈在请求数据的时候失败了...')
	
	except:
		await session.send('吾辈一直在努力尝试和主服取得通信ing...ERROR')